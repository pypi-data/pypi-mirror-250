from typing import Any
from pydantic import BaseModel


class ApiResponse(BaseModel):
    code: int
    data: dict[str, Any]
    error: str | None
