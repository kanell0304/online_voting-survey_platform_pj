from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from backend.app.database.models.image import Image
from backend.app.database.database import get_db
from backend.app.database.schemas.image import ImageResponse
import io

from backend.app.service.image import ImageService

router=APIRouter()

# 이미지 업로드
@router.post("/upload", response_model=ImageResponse)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    result = ImageService.image_upload(file, db)
    return result

# 이미지 조회
@router.get("/image/{image_id}")
def get_image_by_id(image_id: int, db: Session = Depends(get_db)):
    result = ImageService.get_image(image_id, db)
    return result

# 이미지 원본 보여주기
@router.get("/image/raw/{image_id}")
def get_image_raw_by_id(image_id: int, db: Session = Depends(get_db)):
    result = ImageService.get_image_raw(image_id, db)
    return result