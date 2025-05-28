from pydantic import BaseModel, Field
from typing import Dict, Optional


class Response(BaseModel):
    message: str = Field(
        ...,
    )
    data: Optional[Dict] = Field(
        None,
        description="Data for response"
    )
