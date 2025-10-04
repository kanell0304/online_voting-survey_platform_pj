from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List

from backend.app.database.models.response_detail import ResponseDetail
from backend.app.database.schemas.response_detail import ResponsesDetailCreate, ResponsesDetailRead


# 응답 질문 결과 생성
async def create_response_detail(db: AsyncSession, responses_detail_create: ResponsesDetailCreate) -> ResponsesDetailRead:
    db_response_detail = ResponseDetail(**responses_detail_create.model_dump())
    db.add(db_response_detail)
    await db.commit()
    await db.refresh(db_response_detail)
    return ResponsesDetailRead.model_validate(db_response_detail)

# 특정 응답 질문 결과 조회
async def get_response_detail_by_id(db: AsyncSession, response_detail_id: int) -> ResponsesDetailRead | None:
    db_response_detail = await db.execute(select(ResponseDetail).where(ResponseDetail.id == response_detail_id))
    result = db_response_detail.scalar_one_or_none()
    return ResponsesDetailRead.model_validate(result) if result else None

# 설문 응답 번호(response_id)로 해당 응답 질문 결과 모두 조회
async def get_response_details_by_response_id(db: AsyncSession, response_id: int) -> List[ResponsesDetailRead]:
    db_response_detail = await db.execute(select(ResponseDetail).where(ResponseDetail.response_id == response_id))
    results = db_response_detail.scalars().all()
    return [ResponsesDetailRead.model_validate(result) for result in results]

# 특정 응답 질문 결과 삭제
async def delete_response_detail_by_id(db: AsyncSession, response_detail_id: int) -> bool:
    result = await db.execute(delete(ResponseDetail).where(ResponseDetail.id == response_detail_id))
    await db.commit()
    return result.rowcount > 0