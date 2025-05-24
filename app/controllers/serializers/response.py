from typing import Dict, Optional
from pydantic import BaseModel, Field


class Response(BaseModel):
    message: str = Field(
        ...,
    )
    data: Optional[Dict] = Field(
        None,
        description="Data for response"
    )
