from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List


class EmailLogsBase(BaseModel):
    recipient_email: EmailStr
    title: str
    content: str


class EmailLogsCreate(EmailLogsBase):
    survey_id: int

class EmailLogsInDB(EmailLogsBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    survey_id: int

    model_config = ConfigDict(from_attributes=True)

class EmailLogsRead(EmailLogsInDB):
    pass

# 다중 이메일 발송 스키마
class EmailLogsBulkCreate(BaseModel):
    recipient_email: List[EmailStr] = Field(..., description="받는 사람 이메일 목록")
    title: str = Field(..., min_length=1, max_length=100, description="이메일 제목")
    content: str = Field(..., min_length=1, max_length=500, description="이메일 내용")
    survey_id: int = Field(..., description="설문지 id")

# 이메일 발송 결과
class EmailSendResponse(BaseModel):
    total: int = Field(..., description="총 발송 시도 건수")
    success_count: int = Field(..., description="성공 건수")
    failed_count: int = Field(..., description="실패 건수")
    survey_link: str = Field(..., description="설문지 링크")
    success_emails: List[str] = Field(default=[], description="성공한 이메일 목록")
    failed_emails: List[str] = Field(default=[], description="실패한 이메일 목록")

# 테스트 이메일 발송
class EmailTestRequest(BaseModel):
    recipient_email: EmailStr = Field(..., description="받는 사람 이메일")
    title: str = Field(..., min_length=1, description="이메일 제목")
    content: str = Field(..., min_length=1, description="이메일 내용")
    survey_id: int = Field(..., description="설문지 ID")
