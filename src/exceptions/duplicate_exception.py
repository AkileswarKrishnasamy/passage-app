from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException
from starlette import status

class DuplicateException(HTTPException):
    def __init__(self, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail, headers)