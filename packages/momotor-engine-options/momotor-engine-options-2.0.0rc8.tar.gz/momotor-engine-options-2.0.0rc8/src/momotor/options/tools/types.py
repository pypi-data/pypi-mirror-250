import typing
from os import PathLike

from typing_extensions import TypeAlias  # Python 3.10+

from .tool import ToolName

PathList: TypeAlias = typing.Optional[typing.Iterable[typing.Union[str, PathLike]]]
PathTuple: TypeAlias = typing.Optional[typing.Tuple[typing.Union[str, PathLike], ...]]
StrPathOrToolName: TypeAlias = typing.Union[str, PathLike, ToolName]
ToolSet: TypeAlias = frozenset[StrPathOrToolName]
ToolRequirements: TypeAlias = typing.Mapping[str, ToolSet]
