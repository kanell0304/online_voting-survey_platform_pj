from pydantic import BaseModel, ConfigDict

class ResponsesDetailBase(BaseModel):
    selected_option_id: int | None
    text_response: str | None

class ResponsesDetailCreate(ResponsesDetailBase):
    response_id: int
    question_id: int

class ResponsesDetailInDB(ResponsesDetailBase):
    id: int
    response_id: int
    question_id: int

    model_config = ConfigDict(from_attributes=True)

class ResponsesDetailRead(ResponsesDetailInDB):
    pass
