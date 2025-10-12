from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SurveyBase(BaseModel):
    title:str=Field(..., max_length=40)
    description:str=Field(..., max_length=100)
    expire_at:Optional[datetime]=None

class SurveyCreate(SurveyBase):
    pass

class SurveyOut(SurveyBase):
    survey_id:int
    user_id:int
    created_at:datetime
    expire_at:Optional[datetime]=None

    class Config:
        from_attributes=True

# 설문 수정용 : 제목, 설명, 마감기한 수정
# class SurveyUpdate(BaseModel):
#     title:Optional[str]
#     description:Optional[str]
#     expire_at:Optional[datetime]