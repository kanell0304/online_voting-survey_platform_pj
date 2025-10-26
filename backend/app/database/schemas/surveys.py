from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, List
from datetime import datetime
from backend.app.database.schemas.survey_question import SurveyQuestionCreate, SurveyQuestionOut

class SurveyBase(BaseModel):
    title:str=Field(..., max_length=40)
    description:str=Field(..., max_length=100)
    expire_at:Optional[datetime]=None
    is_public:bool=False

class SurveyCreate(SurveyBase):
    questions:List[SurveyQuestionCreate]=Field(default_factory=list)

class SurveyOut(SurveyBase):
    survey_id:int
    user_id:int
    title:str
    description:str
    created_at:datetime
    expire_at:Optional[datetime]=None
    updated_at:Optional[datetime]=None
    is_public:bool=False
    questions:List[SurveyQuestionOut]=Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)

class SurveyUpdate(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None
    expire_at:Optional[datetime]=None
    updated_at:Optional[datetime]=None

    @model_validator(mode="after")
    def include_at_least_one_field(self):
        if all(getattr(self, f) is None for f in ("title", "description", "expire_at")):
            raise ValueError("입력된 변경사항이 없습니다.")
        return self