from pydantic import BaseModel, Field, ConfigDict


class SurveyOptionBase(BaseModel):
    option_text:str=Field(...,max_length=100)

class SurveyOptionCreate(SurveyOptionBase):
    pass

class SurveyOptionOut(SurveyOptionBase):
    option_id:int

    model_config = ConfigDict(from_attributes=True)