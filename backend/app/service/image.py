from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from backend.app.database.models.image import Image
from backend.app.database.database import get_db
import io

class ImageService:

    @staticmethod
    async def image_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
        contents = await file.read()  # 업로드된 파일을 읽어옴
        db_image = Image(filename=file.filename, data=contents)
        db.add(db_image)  # db를 db세션에 추가
        db.commit()
        db.refresh(db_image)
        return db_image

    @staticmethod
    def get_image(image_id: int, db: Session = Depends(get_db)):
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            return JSONResponse(status_code=404, content={"message": "Image not found"})
        return JSONResponse(
            content={"filename": db_image.filename, "data": db_image.data.hex()}
        )

    @staticmethod
    def get_image_raw(image_id: int, db: Session = Depends(get_db)):
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            return JSONResponse(status_code=404, content={"message": "Image not found"})

        # 파일 확장자에 따라 mime-type 변경 가능 (png, jpg 구분)
        return StreamingResponse(  # 바이트 데이터를 바로 이미지 파일로 스트리밍
            io.BytesIO(db_image.data),  # db에서 읽은 바이트 데이터를 파일처럼 전달하기 위해
            media_type="image/png"  # jpg라면 "image/jpeg"
        )