from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List
from backend.app.database.models.responses import Response
from backend.app.database.schemas.responses import ResponsesCreate, ResponsesRead

# 응답 결과 생성
async def create_response(db: AsyncSession, responses_create: ResponsesCreate) -> ResponsesRead:
    db_responses = Response(**responses_create.model_dump())
    db.add(db_responses)
    await db.commit()
    await db.refresh(db_responses)
    return ResponsesRead.model_validate(db_responses)

# 설문지번호로 특정 응답 결과 모두 조회
async def get_response_by_survey_id(db: AsyncSession, survey_id: int) -> List[ResponsesRead]:
    db_responses = await db.execute(select(Response).where(Response.survey_id == survey_id))
    results = db_responses.scalars().all()
    return [ResponsesRead.model_validate(result) for result in results]

# 특정 응답 결과 조회
async def get_response_by_id(db: AsyncSession, response_id: int) -> ResponsesRead | None:
    db_responses = await db.execute(select(Response).where(Response.id == response_id))
    result = db_responses.scalar_one_or_none()
    return ResponsesRead.model_validate(result) if result else None

# 특정 응답 결과 삭제
async def delete_response_by_id(db: AsyncSession, response_id: int) -> bool:
    result = await db.execute(delete(Response).where(Response.id == response_id))
    await db.commit()
    return result.rowcount > 0