import asyncio
import base64
import importlib
import weakref
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING, Callable, Dict, Mapping, Optional, Set, Tuple
from urllib.parse import urlparse

import aiobotocore.client
import aiobotocore.session
import cachetools
import numpy as np
from aiobotocore.config import AioConfig
from botocore import UNSIGNED

from arraylake.asyn import close_async_context, get_loop, sync
from arraylake.chunkstore.abc import Chunkstore
from arraylake.config import config
from arraylake.log_util import get_logger
from arraylake.types import ChunkHash, ReferenceData

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


logger = get_logger(__name__)

MAX_INLINE_THRESHOLD_BYTES = 512


class InlineTooLongError(ValueError):
    pass


def decode_inline_data(data: bytes) -> str:
    """called before writing inline data to json"""
    # matches kerchunk inline output
    try:
        dec = data.decode()
    except UnicodeDecodeError:
        dec = "base64:" + base64.b64encode(data).decode()

    if len(dec) > MAX_INLINE_THRESHOLD_BYTES:
        # if decoding pushed the length over the threshold, raise an error
        raise InlineTooLongError(f"Inline data too large: {len(dec)} > {MAX_INLINE_THRESHOLD_BYTES}")

    return f"inline://{dec}"


def encode_inline_data(data: str) -> bytes:
    """called when loading an inline chunk"""

    if data.startswith("inline://"):
        data = data[9:]

    if data.startswith("base64:"):
        enc = base64.b64decode(data[7:])
    else:
        enc = data.encode()
    return enc


# Below we set up a global cache for aiobotocore clients
# There should be one per each event loop and set of configuration parameters
# dicts aren't hashable, so we sort the keywords into key / value pairs
@dataclass(eq=True, frozen=True)
class ClientKey:
    loop: asyncio.AbstractEventLoop
    client_kwargs: Tuple[Tuple[str, str], ...]


# tried making these weakref.WeakValueDictionary(), but they were getting garbage collected too early
# TODO: investigate whether use of weakref would be more efficient here
# As is, the clients are cleaned up at the end of the python interpreter session.
_GLOBAL_CLIENTS: Dict[ClientKey, "S3Client"] = {}

# this is a cache to use hold asyncio tasks so they are not garbage collected before finishing
background_tasks: Set[asyncio.Task] = set()


async def get_client(loop: asyncio.AbstractEventLoop, **client_kws) -> "S3Client":
    """
    Attempt to get an aws client for a specific event loop and set of parameters.
    If the client already exists, the global cache will be used.
    If not, a new client will be created.
    """

    key = ClientKey(loop, tuple(sorted(client_kws.items())))
    logger.debug("%d s3 clients present in cache.", len(_GLOBAL_CLIENTS))
    if key not in _GLOBAL_CLIENTS:
        logger.debug("Creating new s3 client %s. Loop id %s.", key, id(loop))
        anon = client_kws.pop("anon", False)
        if anon:
            client_kws["config"] = AioConfig(signature_version=UNSIGNED)
        client_creator: "S3Client" = aiobotocore.session.get_session().create_client("s3", **client_kws)
        new_client = await client_creator.__aenter__()
        weakref.finalize(new_client, close_client, key)
        _GLOBAL_CLIENTS[key] = new_client
    else:
        logger.debug("Client %s already present. Loop id %s.", key, id(loop))
    return _GLOBAL_CLIENTS[key]


def close_client(key: ClientKey) -> None:
    """
    This is a finalizer function that is called when a global client is
    garbage collected. It cleanly closes the client for the specified key.

    If the event loop associated with this client is already closed, we can't
    call __aexit__. So we attempt to directly close the TCP Socket associated
    with the aiohttp session.

    If the event loop associated with this client is determined to be the
    dedicated io loop, we call `sync` to on __aexit__.

    If the event loop associated with this client is determined to be the currently
    running event loop, we schedule the __aexit__ coroutine for execution.

    If the event loop doesn't match any of these scenarios, we have no way to call
    the closer function and issue a RuntimeWarning

    Note: logging in this function runs the risk of conflicting with pytest#5502. For
    this reason, we have removed debug log statements.
    """
    client = _GLOBAL_CLIENTS.pop(key)

    client_loop = key.loop  # the loop this client was created from

    if not hasattr(client, "_endpoint"):
        return  # this makes mypy happy

    # this is the underlying thing we have to close
    aio_http_session = client._endpoint.http_session._session
    # sanity checks
    # assert aio_http_session._loop is client_loop
    # assert aio_http_session._connector._loop is client_loop

    if aio_http_session.closed:
        return

    sync_loop = get_loop()  # the loop associated with the synchronizer thread

    try:
        running_loop = asyncio.get_running_loop()
    except RuntimeError:
        running_loop = None

    if client_loop.is_closed():
        # we can never talk to this client again because its loop is closed;
        # just close the sockets directly
        aio_http_session._connector._close()
        assert aio_http_session.closed
    else:
        # client loop is still open -- how can we talk to it?
        if client_loop is sync_loop:
            sync(close_async_context, client, "calling from sync", timeout=1)
        elif client_loop is running_loop:
            coro = close_async_context(client, f"closing from loop {id(client_loop)}")
            if client_loop.is_running():
                task = client_loop.create_task(coro)
                # try to prevent this task from being garbage collected before it finishes
                background_tasks.add(task)
            else:
                client_loop.run_until_complete(coro)


class HashValidationError(AssertionError):
    pass


def tokenize(data: bytes, *, hasher: Callable) -> str:
    hash_obj = hasher(data)
    return hash_obj.hexdigest()


@lru_cache(maxsize=None)
def get_hasher(method):
    try:
        mod_name, func_name = method.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        return getattr(mod, func_name)
    except (ImportError, AttributeError):
        raise ValueError(f"invalid hash method {method}")


class S3Chunkstore(Chunkstore):
    """S3Chunkstore interface"""

    bucket_name: str
    prefix: str
    use_relative_addressing: bool
    inline_threshold_bytes: int
    client_kws: Mapping[str, str]
    _OPEN: bool
    _session_client: Optional["S3Client"]
    _known_key_cache: cachetools.LFUCache

    def __init__(self, bucket_name: str, prefix: str, use_relative_addressing: bool, inline_threshold_bytes: int = 0, **client_kws):
        """
        Args:
            bucket_name: The bucket in which to store chunks data.
            prefix: a string under which all chunk keys will be placed. Must be unique for the bucket.
            use_relative_addressing: if True, use the modern encoding that stores only the hash and takes
                bucket_name and prefix from the repo's bucket. If False, use the full uri stored in old
                style ReferenceData.
            inline_threshold_bytes: Byte size below which a chunk will be stored in the metastore database. Maximum is 512.
                Values less than or equal to 0 disable inline storage.
            client_kws: Additional keyword arguments to pass to
                ``aiobotocore.session.AIOSession.session.create_client``, by default None.
        """
        assert prefix or not use_relative_addressing, "S3Chunkstore in relative addressing mode requires a prefix"
        self.bucket_name = bucket_name.strip("/")
        self.prefix = prefix.strip("/")
        self.use_relative_addressing = use_relative_addressing
        self.client_kws = client_kws
        self._set_props()
        self._setup_chunk_key_cache()

        self.inline_threshold_bytes = inline_threshold_bytes

        if self.inline_threshold_bytes > MAX_INLINE_THRESHOLD_BYTES:
            raise ValueError(f"Inline chunk threshold too large, max={MAX_INLINE_THRESHOLD_BYTES} bytes")

    def _set_props(self):
        self._session_client = None

    def __getstate__(self):
        return self.bucket_name, self.prefix, self.use_relative_addressing, self.inline_threshold_bytes, self.client_kws

    def __setstate__(self, state):
        self.bucket_name, self.prefix, self.use_relative_addressing, self.inline_threshold_bytes, self.client_kws = state
        self._set_props()
        self._setup_chunk_key_cache()

    async def _open(self):
        if self._session_client is not None:
            return
        loop = asyncio.get_running_loop()
        self._session_client = await get_client(loop, **self.client_kws)

    def _setup_chunk_key_cache(self):
        self._known_key_cache = cachetools.LFUCache(maxsize=5000)  # tunable

    def __repr__(self):
        status = "OPEN" if self._session_client is not None else "CLOSED"
        return (
            f"<arraylake.s3_chunkstore.S3Chunkstore "
            f"bucket_name='{self.bucket_name}' "
            f"prefix='{self.prefix}' "
            f"use_relative_addressing='{self.use_relative_addressing}' "
            f"status={status}>"
        )

    async def ping(self):
        """Check if the chunk store bucket exists."""
        await self._open()
        # Mypy cannot tell that self._session_cleint is not None (set it self._open())
        # Note: this can likely be removed once we drop support for Python 3.8
        if self._session_client is None:
            raise ValueError("session client not set")
        # TODO: Should raise an exception if the bucket does not exist
        await self._session_client.head_bucket(Bucket=self.bucket_name)

    async def add_chunk(self, data: bytes, *, hash_method: Optional[str] = None) -> ReferenceData:
        await self._open()
        # Mypy cannot tell that self._session_cleint is not None (set it self._open())
        # Note: this can likely be removed once we drop support for Python 3.8
        if self._session_client is None:
            raise ValueError("session client not set")
        if isinstance(data, np.ndarray):
            # We land here if the data are not compressed by a codec. This happens for 0d arrays automatically.
            data = data.tobytes()

        if hash_method is None:
            hash_method = config.get("chunkstore.hash_method", "hashlib.sha256")

        hasher = get_hasher(hash_method)
        token = tokenize(data, hasher=hasher)
        hash = ChunkHash(method=hash_method, token=token)
        length = len(data)

        inline = False
        uri: Optional[str] = None
        if length <= self.inline_threshold_bytes:
            await logger.adebug("Adding inline chunk %s", token)
            try:
                uri = decode_inline_data(data)
                inline = True
            except InlineTooLongError:
                # we failed to inline this data, so treat it like a regular chunk
                pass

        schema_version = None
        if inline is False:
            await logger.adebug("Adding s3 chunk %s", token)
            key = self._make_key(token=token)

            if self.use_relative_addressing:
                schema_version = 1
            else:
                uri = f"s3://{self.bucket_name}/{key}"

            if token not in self._known_key_cache:
                resp = await self._session_client.put_object(Bucket=self.bucket_name, Key=key, Body=data)
                self._known_key_cache[token] = None
                await logger.adebug(resp)

        return ReferenceData(uri=uri, offset=0, length=length, hash=hash, v=schema_version)

    async def _pull_data(self, start_byte: int, length: int, key: str, bucket: str) -> bytes:
        assert self._session_client, "get_chunk must open chunkstore"
        # stop_byte is inclusive, in contrast to python indexing conventions
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Range
        stop_byte = start_byte + length - 1
        byte_range = f"bytes={start_byte}-{stop_byte}"
        response = await self._session_client.get_object(Bucket=bucket, Key=key, Range=byte_range)
        await logger.adebug(response)
        async with response["Body"] as stream:
            data = await stream.read()
        return data

    def _make_key(self, token: str) -> str:
        # Notice that the hash_method in the key is a recent addition, so we
        # probably have two different formats, even within the same repositories
        # We added in the unlikely case that there are collisions between different hashing methods
        if self.prefix:
            return f"{self.prefix}/{token}"
        else:
            return token

    def _make_key_from_chunk_ref(self, chunk_ref: ReferenceData) -> str:
        hash = chunk_ref.hash
        assert hash, "Relative path chunk manifests must have a hash"
        token = hash.get("token")
        assert token, "Relative path chunk manifests must have a token"
        return self._make_key(token=token)

    async def _get_relative_chunk(self, chunk_ref: ReferenceData) -> Tuple[str, bytes]:
        if chunk_ref.uri is not None:
            # We are a relative chunstore, fetching a virtual chunk
            return await self._get_absolute_chunk(chunk_ref)

        key = self._make_key_from_chunk_ref(chunk_ref)
        data = await self._pull_data(start_byte=chunk_ref.offset, length=chunk_ref.length, key=key, bucket=self.bucket_name)
        return key, data

    async def _get_absolute_chunk(self, chunk_ref: ReferenceData) -> Tuple[str, bytes]:
        if chunk_ref.uri is None:
            raise ValueError("Invalid chunk for absolute path S3Chunkstore, it should have a uri")
        parsed_uri = urlparse(chunk_ref.uri)
        key = parsed_uri.path.strip("/")
        bucket = parsed_uri.netloc
        data = await self._pull_data(start_byte=chunk_ref.offset, length=chunk_ref.length, key=key, bucket=bucket)
        return key, data

    async def get_chunk(self, chunk_ref: ReferenceData, *, validate: bool = False) -> bytes:
        await self._open()
        # Mypy cannot tell that self._session_client is not None (set it self._open())
        # Note: this can likely be removed once we drop support for Python 3.8
        if self._session_client is None:
            raise ValueError("session client not set")
        logger.debug("get_chunk %s", chunk_ref)

        if chunk_ref.uri is not None and chunk_ref.uri.startswith("inline://"):
            # chunk is inline
            key = chunk_ref.uri
            data = encode_inline_data(chunk_ref.uri)
        else:
            # chunk is on s3
            if self.use_relative_addressing and chunk_ref.v is not None and chunk_ref.v > 0:
                key, data = await self._get_relative_chunk(chunk_ref)
            else:
                key, data = await self._get_absolute_chunk(chunk_ref)

        if validate:
            if chunk_ref.hash is None:
                raise ValueError("chunk hash not set, cannot validate")
            hasher = get_hasher(chunk_ref.hash["method"])
            h = tokenize(data, hasher=hasher)
            if h != chunk_ref.hash["token"]:
                raise HashValidationError(f"hashes did not match for key: {key}")

        return data
