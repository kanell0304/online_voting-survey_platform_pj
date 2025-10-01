from pydantic import BaseModel

class ImageResponse(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True  #sqlalchemy orm객체 받아서 변환 가능하게 설정