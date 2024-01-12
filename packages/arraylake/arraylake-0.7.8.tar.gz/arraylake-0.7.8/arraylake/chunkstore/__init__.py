from typing import Optional
from urllib.parse import urlparse

from arraylake.chunkstore.abc import Chunkstore
from arraylake.chunkstore.s3chunkstore import MAX_INLINE_THRESHOLD_BYTES, S3Chunkstore
from arraylake.types import DBID, Bucket


def mk_chunkstore_from_uri(chunkstore_uri: str, inline_threshold_bytes: int = 0, **kwargs) -> Chunkstore:
    """Initialize a Chunkstore

    Args:
        chunkstore_uri: URI to chunkstore.
        inline_threshold_bytes: Byte size below which a chunk will be stored in the metastore database. Maximum is 512.
            Values less than or equal to 0 disable inline storage.
        kwargs: Additional keyword arguments to pass to the chunkstore constructor.
    Returns:
        chunkstore:
    """
    if chunkstore_uri.startswith("s3://"):
        parsed_uri = urlparse(chunkstore_uri)
        bucket_name = parsed_uri.netloc.strip("/")
        prefix = parsed_uri.path.strip("/")

        return S3Chunkstore(
            bucket_name=bucket_name,
            prefix=prefix,
            use_relative_addressing=False,
            inline_threshold_bytes=inline_threshold_bytes,
            **kwargs,
        )
    else:
        raise ValueError(f"Cannot parse chunkstore uri {chunkstore_uri}, supported prefixes are: ['s3://']")


def mk_chunkstore_from_bucket_config(bucket: Bucket, repo_id: DBID, inline_threshold_bytes: int = 0, **kwargs) -> Chunkstore:
    bucket_name = bucket.name
    prefix = repo_id.hex()
    client_kws = dict(bucket.extra_config)
    if bucket.endpoint_url is not None:
        client_kws["endpoint_url"] = bucket.endpoint_url
    return S3Chunkstore(
        bucket_name=bucket_name,
        prefix=prefix,
        use_relative_addressing=True,
        inline_threshold_bytes=inline_threshold_bytes,
        **{**client_kws, **kwargs},
    )
