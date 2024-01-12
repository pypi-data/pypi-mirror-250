import os
import typing

T = typing.TypeVar("T")

Cast = typing.Union[typing.Callable[[str], T], int, float, str, bool]
Path = typing.Union[str, os.PathLike[str]]
OpenPath = typing.Union[int, typing.Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]]
Config = typing.Dict[str, str]
