from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from backend.app.database.schemas.survey_question import SurveyQuestionCreate, SurveyQuestionOut

class SurveyBase(BaseModel):
    title:str=Field(..., max_length=40)
    description:str=Field(..., max_length=100)
    expire_at:Optional[datetime]=None

class SurveyCreate(SurveyBase):
    questions:List[SurveyQuestionCreate]=Field(default_factory=list)

class SurveyOut(SurveyBase):
    survey_id:int
    user_id:int
    created_at:datetime
    expire_at:Optional[datetime]=None
    questions:List[SurveyQuestionOut]=Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)

# 설문 수정용 : 제목, 설명, 마감기한 수정
# class SurveyUpdate(BaseModel):
#     title:Optional[str]
#     description:Optional[str]
#     expire_at:Optional[datetime]