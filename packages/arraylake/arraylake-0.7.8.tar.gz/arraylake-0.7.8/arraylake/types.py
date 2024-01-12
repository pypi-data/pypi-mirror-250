import datetime
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Iterator, List, Mapping, NewType, Optional, Tuple, Union
from uuid import UUID

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    root_validator,
    validator,
)
from pydantic.json import timedelta_isoformat
from typing_extensions import TypedDict

if sys.version_info >= (3, 11):
    # python 3.11+
    from enum import StrEnum
else:

    class StrEnum(str, Enum):
        pass


def utc_now():
    # drop microseconds because bson does not support them
    return datetime.datetime.utcnow().replace(microsecond=0)


class DBID(bytes):
    """
    A database ID.

    Used to represent the ids of objects that live in a database. It can be
    used with BaseModel, and knows how to validate and convert from str,
    other bytes and anything that has a `binary` property.
    """

    def __str__(self):
        """Format as hex digits"""
        return self.hex()

    # We implement a __repr__ that is not valid python code but won't
    # confuse the users. They want to see a simple hex id.
    __repr__ = __str__

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]):
        field_schema.update(type="string")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate and convert from other types.

        Can convert:
          from str: reading hex characters
          from bytes: retaining the immutable binary input
          from objects with a binary property:
        """
        if isinstance(v, str):
            return DBID.fromhex(v)
        if isinstance(v, bytes):
            return DBID(v)
        if hasattr(v, "binary"):
            return DBID(v.binary)
        raise ValueError("Invalid DBID object")


# These are type aliases, which allow us to write e.g. Path instead of str. Since they can be used interchangeably,
# I'm not sure how useful they are.

CommitID = DBID
Path = str
MetastoreUrl = Union[AnyUrl, AnyHttpUrl]

# These are used by mypy in static typing to ensure logical correctness but cannot be used at runtime for validation.
# They are more strict than the aliases; they have to be explicitly constructed.

SessionID = NewType("SessionID", str)
TagName = NewType("TagName", str)
BranchName = NewType("BranchName", str)

CommitHistory = Iterator[CommitID]


class BulkCreateDocBody(BaseModel):
    session_id: SessionID
    content: Mapping[str, Any]
    path: Path


class CollectionName(StrEnum):
    sessions = "sessions"
    metadata = "metadata"
    chunks = "chunks"
    nodes = "nodes"


class ChunkHash(TypedDict):
    method: str
    token: str


class SessionType(StrEnum):
    read_only = "read"
    write = "write"


class SessionBase(BaseModel):
    # NOTE: branch is Optional to accommodate workflows where a particular
    # commit is checked out.
    branch: Optional[BranchName]
    base_commit: Optional[CommitID]
    # TODO: Do we bite the bullet and replace all these author_name/author_email
    # properties with principal_id?
    author_name: Optional[str] = None
    author_email: EmailStr
    message: Optional[str]
    session_type: SessionType

    class Config:
        json_encoders = {DBID: str}

    @root_validator(pre=True)
    def _one_of_branch_or_commit(cls, values):
        if not values.get("branch") and not values.get("base_commit"):
            raise ValueError("At least one of branch or base_commit must not be None")
        return values


class NewSession(SessionBase):
    expires_in: datetime.timedelta

    class Config:
        json_encoders = {datetime.timedelta: timedelta_isoformat}


class SessionInfo(SessionBase):
    id: SessionID = Field(alias="_id")
    start_time: datetime.datetime
    expiration: datetime.datetime

    class Config:
        allow_population_by_field_name = True


class SessionExpirationUpdate(BaseModel):
    session_id: SessionID
    expires_in: datetime.timedelta

    class Config:
        json_encoders = {datetime.timedelta: timedelta_isoformat}


# These are the Pydantic models. They can be used for both validation and typing.
# Presumably it is considerably more expensive to use a BaseModel than just a dict.


class ModelWithID(BaseModel):
    id: DBID = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {DBID: str}


class RepoCreateBody(BaseModel):
    name: str
    description: Optional[str] = None
    bucket_nickname: Optional[str] = None


class RepoVisibility(str, Enum):
    # PRIVATE: Visible only to repo members.
    # NOTE: Currently, this means any member of an org.
    PRIVATE = "PRIVATE"

    # AUTHENTICATED_PUBLIC: Visible to any authenticated user of Arraylake.
    AUTHENTICATED_PUBLIC = "AUTHENTICATED_PUBLIC"

    # PUBLIC: Visible to anybody on the public internet.
    # PUBLIC = "PUBLIC"


class Bucket(BaseModel):
    id: UUID
    nickname: str
    platform: str
    name: str
    endpoint_url: Optional[str]
    extra_config: Mapping[str, Any]


class Repo(ModelWithID):
    org: str
    name: str
    created: datetime.datetime = Field(default_factory=utc_now)
    description: Optional[str] = None
    created_by: Optional[UUID] = None
    visibility: RepoVisibility = RepoVisibility.PRIVATE
    bucket: Optional[Bucket] = None

    class Config:
        json_encoders = {DBID: str, datetime.datetime: lambda x: x.isoformat(), UUID: str}

    def _asdict(self):
        """custom dict method ready to be serialized as json"""
        d = self.dict()
        d["id"] = str(d["id"])
        d["created"] = d["created"].isoformat()
        if self.created_by is not None:
            d["created_by"] = str(d["created_by"])
        return d

    def __repr__(self):
        return f"<Repo {self.org}/{self.name} created {self.created} by {self.created_by}>"


class Author(BaseModel):
    name: Optional[str] = None
    email: EmailStr

    # TODO: Harmonize this with Commit.author_entry() for DRY.
    def entry(self) -> str:
        if self.name:
            return f"{self.name} <{self.email}>"
        else:
            return f"<{self.email}>"


class NewCommit(BaseModel):
    session_id: SessionID
    session_start_time: datetime.datetime
    parent_commit: Optional[CommitID] = None
    commit_time: datetime.datetime
    author_name: Optional[str] = None
    author_email: EmailStr
    # TODO: add constraints once we drop python 3.8
    # https://github.com/pydantic/pydantic/issues/156
    message: str

    class Config:
        json_encoders = {DBID: str}


# TODO: remove duplication with NewCommit. Redefining these attributes works around this error:
# Definition of "Config" in base class "ModelWithID" is incompatible with definition in base class "NewCommit"
class Commit(ModelWithID):
    session_start_time: datetime.datetime
    parent_commit: Optional[CommitID] = None
    commit_time: datetime.datetime
    author_name: Optional[str]
    author_email: EmailStr
    # TODO: add constraints once we drop python 3.8
    # https://github.com/pydantic/pydantic/issues/156
    message: str

    def author_entry(self):
        if self.author_name:
            return f"{self.author_name} <{self.author_email}>"
        else:
            return f"<{self.author_email}>"


class Branch(BaseModel):
    id: BranchName = Field(alias="_id")
    commit_id: CommitID

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {DBID: str}


class Tag(BaseModel):
    id: TagName = Field(alias="_id")
    commit_id: CommitID

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {DBID: str}


@dataclass
class DocResponse:
    id: str  # not DBID
    session_id: SessionID
    path: Path
    content: Optional[Mapping[str, Any]] = None
    deleted: bool = False

    def __post_init__(self):
        checks = [
            isinstance(self.id, str),
            # session_id: Cannot use isinstance() with NewType, so we use str
            isinstance(self.session_id, str),
            isinstance(self.path, Path),
            isinstance(self.deleted, bool),
            isinstance(self.content, dict) if self.content else True,
        ]
        if not all(checks):
            raise ValueError(f"Validation failed {self}, {checks}")


class DocSessionsResponse(ModelWithID):
    session_id: SessionID
    deleted: bool = False
    chunksize: int = 0


class SessionPathsResponse(ModelWithID):
    path: Path
    deleted: bool = False


class ReferenceData(BaseModel):
    uri: Optional[str]  # will be None in non-virtual new style repos
    offset: int
    length: int
    hash: Optional[ChunkHash]
    # Schema version
    v: Optional[int]

    @root_validator(pre=True)
    def _one_of_uri_or_hash(cls, values):
        if not values.get("uri") and not values.get("hash"):
            raise ValueError("At least one of uri or hash must not be None")
        return values

    @validator("v", pre=True)
    def _supported_versions(cls, value):
        supported_versions = {None, 1}
        if value not in supported_versions:
            raise ValueError(f"ReferenceData version not supported. Must be one of {supported_versions}")
        return value


class UpdateBranchBody(BaseModel):
    branch: BranchName
    new_commit: CommitID
    new_branch: bool = False
    base_commit: Optional[CommitID] = None

    # TODO: Make session_id mandatory once all clients are using
    # managed_sessions by default.
    session_id: Optional[SessionID] = None

    class Config:
        json_encoders = {DBID: str}


class OauthTokensResponse(BaseModel):
    access_token: SecretStr
    id_token: SecretStr
    refresh_token: Optional[SecretStr] = None
    expires_in: int
    token_type: str

    def dict(self, **kwargs):
        """custom dict that drops default values"""
        tokens = super().dict(**kwargs)
        # special case: drop refresh token if it is None
        if not tokens.get("refresh_token", 1):
            del tokens["refresh_token"]
        return tokens

    class Config:
        json_encoders = {SecretStr: lambda v: v.get_secret_value() if v else None}


class OauthTokens(OauthTokensResponse):
    refresh_token: SecretStr

    def dict(self, **kwargs):
        """custom dict method that decodes secrets"""
        tokens = super().dict(**kwargs)
        for k, v in tokens.items():
            if isinstance(v, SecretStr):
                tokens[k] = v.get_secret_value()
        return tokens

    def __hash__(self):
        return hash((self.access_token, self.id_token, self.refresh_token, self.expires_in, self.token_type))


class UserInfo(BaseModel):
    id: UUID
    first_name: Union[str, None] = None
    family_name: Union[str, None] = None
    email: EmailStr

    def as_author(self) -> Author:
        return Author(name=f"{self.first_name} {self.family_name}", email=self.email)


class ApiTokenInfo(BaseModel):
    id: UUID
    client_id: str
    email: EmailStr
    expiration: int

    def as_author(self) -> Author:
        return Author(email=self.email)


class PathSizeResponse(BaseModel):
    path: Path
    number_of_chunks: int
    total_chunk_bytes: int


class Array(BaseModel):
    attributes: Dict[str, Any] = {}
    chunk_grid: Dict[str, Any] = {}
    chunk_memory_layout: Optional[str] = None
    compressor: Union[Dict[str, Any], None] = None
    data_type: Union[str, Dict[str, Any], None] = None
    fill_value: Any = None
    extensions: list = []
    shape: Optional[Tuple[int, ...]] = None


# Utility to coerce Array data types to string version
def get_array_dtype(arr: Array) -> str:
    import numpy as np

    if isinstance(arr.data_type, str):
        return str(np.dtype(arr.data_type))
    elif isinstance(arr.data_type, dict):
        return str(arr.data_type["type"])
    else:
        raise ValueError(f"unexpected array type {type(arr.data_type)}")


class Tree(BaseModel):
    trees: Dict[str, "Tree"] = {}
    arrays: Dict[str, Array] = {}
    attributes: Dict[str, Any] = {}

    def _as_rich_tree(self, name: str = "/"):
        from rich.jupyter import JupyterMixin
        from rich.tree import Tree as _RichTree

        class RichTree(_RichTree, JupyterMixin):
            pass

        def _walk_and_format_tree(td: Tree, tree: _RichTree) -> _RichTree:
            for key, group in td.trees.items():
                branch = tree.add(f":file_folder: {key}")
                _walk_and_format_tree(group, branch)
            for key, arr in td.arrays.items():
                dtype = get_array_dtype(arr)
                tree.add(f":regional_indicator_a: {key} {arr.shape} {dtype}")
            return tree

        return _walk_and_format_tree(self, _RichTree(name))

    def __rich__(self):
        return self._as_rich_tree()

    def _as_ipytree(self, name: str = ""):
        from ipytree import Node
        from ipytree import Tree as IpyTree

        def _walk_and_format_tree(td: Tree) -> List[Node]:
            nodes = []
            for key, group in td.trees.items():
                _nodes = _walk_and_format_tree(group)
                node = Node(name=key, nodes=_nodes)
                node.icon = "folder"
                node.opened = False
                nodes.append(node)
            for key, arr in td.arrays.items():
                dtype = get_array_dtype(arr)
                node = Node(name=f"{key} {arr.shape} {dtype}")
                node.icon = "table"
                node.opened = False
                nodes.append(node)
            return nodes

        nodes = _walk_and_format_tree(self)
        node = Node(name=name, nodes=nodes)
        node.icon = "folder"
        node.opened = True
        tree = IpyTree(nodes=[node])

        return tree

    def _repr_mimebundle_(self, **kwargs):
        try:
            _tree = self._as_ipytree(name="/")
        except ImportError:
            try:
                _tree = self._as_rich_tree(name="/")
            except ImportError:
                return repr(self)
        return _tree._repr_mimebundle_(**kwargs)


class UserDiagnostics(BaseModel):
    system: Optional[Dict[str, str]] = None
    versions: Optional[Dict[str, str]] = None
    config: Optional[Dict[str, str]] = None
    service: Optional[Dict[str, str]] = None
