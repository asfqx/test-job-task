from pydantic import BaseModel
from typing import Optional


class GetBankResponse(BaseModel):
    success: bool
    result: Optional[dict] = None
    detail: Optional[str] = None


