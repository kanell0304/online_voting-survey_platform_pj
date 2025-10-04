from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

# API 기본 형식입니다 복사해서 쓰셔도 되요

router = APIRouter(prefix="/preset", tags=["Preset"])

@router.post("/create", response_model=None)
async def create_api(object_create: None, db: AsyncSession):
    return None

@router.get("/get_all", response_model=None)
async def get_all_api(db: AsyncSession):
    return None

@router.get("/get_one", response_model=None)
async def get_one_api(object_id: int, db: AsyncSession):
    return None

@router.put("/edit/{object_id}", response_model=None)
async def put_api(object_id: int, db: AsyncSession):
    return None

@router.delete("/delete/{object_id}", response_model=None)
async def delete_api(object_id: int, db: AsyncSession):
    return None