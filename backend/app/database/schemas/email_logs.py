from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List


class EmailLogsBase(BaseModel):
    received_email: EmailStr
    title: str
    content: str


class EmailLogsCreate(EmailLogsBase):
    survey_id: int


class EmailLogsBulkCreate(BaseModel):
    survey_id: int
    title: str
    content: str
    recipients: List[EmailStr]


class EmailLogsInDB(EmailLogsBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    survey_id: int

    model_config = ConfigDict(from_attributes=True)


class EmailLogsRead(EmailLogsInDB):
    pass


class EmailSendResponse(BaseModel):
    total: int
    success_count: int
    failed_count: int
    survey_link: str
    success_emails: List[str] = []
    failed_emails: List[dict] = []


class EmailTestRequest(BaseModel):
    recipient: EmailStr
    title: str = "테스트 이메일"
    content: str = "이것은 테스트 이메일입니다."
    survey_id: int = 1
