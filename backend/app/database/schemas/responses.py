from datetime import datetime, timezone
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.database.schemas.response_detail import ResponsesDetailCreate, ResponsesDetailRead


class ResponsesBase(BaseModel):
    pass

class ResponsesCreate(ResponsesBase):
    survey_id: int
    user_id: str
    details: List[ResponsesDetailCreate]

class ResponsesInDB(ResponsesBase):
    id: int
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    survey_id: int
    user_id: str
    details: List[ResponsesDetailRead]

    model_config = ConfigDict(from_attributes=True)

class ResponsesRead(ResponsesInDB):
    pass
