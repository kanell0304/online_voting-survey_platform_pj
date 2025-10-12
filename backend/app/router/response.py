from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.database import get_db
from backend.app.database.schemas.response_detail import ResponsesDetailRead, ResponsesDetailCreate
from backend.app.database.schemas.responses import ResponsesRead, ResponsesCreate
from backend.app.service.response_service import ResponseService

router = APIRouter(prefix="/responses", tags=["Responses"])

# =================== ResponseDetail ===================

# 단일 response_detail 생성
@router.post("/response_detail/create", response_model=ResponsesDetailRead)
async def create_response_detail(response_detail_create: ResponsesDetailCreate, db: AsyncSession = Depends(get_db)):
    result = await ResponseService.create_response_detail(response_detail_create, db)
    return result

# 특정 response_id의 모든 response_details 조회
@router.get("/response_detail/response_id/{response_id}", response_model=List[ResponsesDetailRead])
async def get_all_response_details_by_response_id(response_id: int, db: AsyncSession = Depends(get_db)):
    result = await ResponseService.get_all_response_details_by_response_id(response_id, db)
    return result

# 모든 response_detail 조회
@router.get("/response_detail", response_model=List[ResponsesDetailRead])
async def get_response_details(db: AsyncSession = Depends(get_db)):
    result = await ResponseService.get_all_response_details(db)
    return result

# 특정 response_detail 조회
@router.get("/response_detail/{response_detail_id}", response_model=ResponsesDetailRead)
async def get_response_detail_by_id(response_detail_id: int, db: AsyncSession = Depends(get_db)):
    result = await ResponseService.get_response_detail_by_id(response_detail_id, db)
    return result

# 특정 response_detail 삭제
@router.delete("/response_detail/{response_detail_id}")
async def delete_response_detail(response_detail_id: int, db: AsyncSession = Depends(get_db)):
    await ResponseService.delete_response_detail(response_detail_id, db)
    return {"msg": "ResponseDetail deleted successfully"}

# =================== Response ===================

# response 생성
@router.post("/create", response_model=ResponsesRead)
async def create_response(response_create: ResponsesCreate, db: AsyncSession = Depends(get_db)):
    result = await ResponseService.create_response(response_create, db)
    return result

# 특정 survey_id의 모든 response 조회
@router.get("/survey_id/{survey_id}", response_model=List[ResponsesRead])
async def get_all_responses_by_survey_id(survey_id: int, db: AsyncSession = Depends(get_db)):
    result = await ResponseService.get_all_responses_by_survey_id(survey_id, db)
    return result

# 특정 user_id의 모든 response 조회
@router.get("/user_id/{user_id}", response_model=List[ResponsesRead])
async def get_all_responses_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await ResponseService.get_all_responses_by_user_id(user_id, db)
    return result

# 특정 response 조회
@router.get("/{response_id}", response_model=ResponsesRead)
async def get_response_by_id(response_id: int, db: AsyncSession = Depends(get_db)):
    result = await ResponseService.get_response_by_id(response_id, db)
    return result

# 모든 responses 조회
@router.get("", response_model=List[ResponsesRead])
async def get_all_responses(db: AsyncSession = Depends(get_db)):
    result = await ResponseService.get_all_responses(db)
    return result

# 특정 response 삭제
@router.delete("/delete/{response_id}")
async def delete_response(response_id: int, db: AsyncSession = Depends(get_db)):
    await ResponseService.delete_response(response_id, db)
    return {"msg": "Response deleted successfully"}

