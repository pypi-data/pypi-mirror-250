from dataclasses import dataclass
from typing import TypeAlias, Literal
from typing import Union, Dict

RESPONSE_STATUS: TypeAlias = Literal[
    "OK",
    "NG",
]


@dataclass
class Response:
    status: RESPONSE_STATUS
    message: str


@dataclass
class ColabInternalFetchResponse(Response):
    url: str
    data: Dict[str, Union[str, int, float]] | None


@dataclass
class EasyFileUploaderResponse(Response):
    allowed_filenames: Dict[str, str] | None = None
