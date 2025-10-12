from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from backend.app.database.models.response_detail import ResponseDetail
from backend.app.database.models.responses import Response
from backend.app.database.schemas.response_detail import ResponsesDetailCreate
from backend.app.database.schemas.responses import ResponsesCreate


class ResponseService:

    # response 생성
    @staticmethod
    async def create_response(response_create: ResponsesCreate, db: AsyncSession):
        response_data = response_create.model_dump(exclude={'details'}) # details를 분리
        db_response = Response(**response_data)

        details_data = response_create.details # details만 작업
        db_response.details = [ResponseDetail(**detail.model_dump(exclude={'response_id'})) for detail in details_data]

        db.add(db_response)
        await db.commit()
        await db.refresh(db_response, attribute_names=['details'])
        return db_response

    # 특정 response 조회
    @staticmethod
    async def get_response_by_id(response_id: int, db: AsyncSession):
        db_response = await db.execute(select(Response).options(selectinload(Response.details)).where(Response.id == response_id)) # details를 함께 조회

        try:
            return db_response.scalar_one()
        except NoResultFound: # 조회 결과가 없으면 NoResultFound 예외 발생
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Response not found")

    # 모든 response 조회
    @staticmethod
    async def get_all_responses(db: AsyncSession):
        result = await db.execute(select(Response).options(selectinload(Response.details)))
        db_responses = result.scalars().all()

        if not db_responses:  # 리스트에 결과가 하나도 없다면 예외 발생
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No responses found")

        return db_responses

    # 특정 survey_id의 모든 response 조회
    @staticmethod
    async def get_all_responses_by_survey_id(survey_id: int, db: AsyncSession):
        result = await db.execute(select(Response).options(selectinload(Response.details)).where(Response.survey_id == survey_id))
        db_responses = result.scalars().all()

        if not db_responses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No responses found")

        return db_responses

    # 특정 user_id의 모든 response 조회
    @staticmethod
    async def get_all_responses_by_user_id(user_id: int, db: AsyncSession):
        result = await db.execute(select(Response).options(selectinload(Response.details)).where(Response.user_id == user_id))
        db_responses = result.scalars().all()

        if not db_responses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No responses found")

        return db_responses

    # 특정 response 삭제
    @staticmethod
    async def delete_response(response_id: int, db: AsyncSession):
        db_response = await db.execute(select(Response).where(Response.id == response_id))
        deleted_response = db_response.scalar_one_or_none()
        if not deleted_response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Response not found")

        await db.delete(deleted_response)
        await db.commit()
        return {"msg": "Response deleted", "deleted response_id": response_id}

# ====================================================================
    # response_detail

    # 단일 response_detail 생성 - 기본적으로 response를 생성할때 함께 생성됨
    @staticmethod
    async def create_response_detail(response_detail_create: ResponsesDetailCreate, db: AsyncSession):
        db_response_detail = ResponseDetail(**response_detail_create.model_dump())
        db.add(db_response_detail)
        await db.commit()
        await db.refresh(db_response_detail)
        return db_response_detail

    # 특정 response_detail 조회
    @staticmethod
    async def get_response_detail_by_id(response_detail_id: int, db: AsyncSession):
        db_response_detail = await db.execute(select(ResponseDetail).where(ResponseDetail.id == response_detail_id))

        try:
            return db_response_detail.scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ResponseDetail not found")

    # 모든 response_details 조회
    @staticmethod
    async def get_all_response_details(db: AsyncSession):
        result = await db.execute(select(ResponseDetail))
        db_response_details = result.scalars().all()

        if not db_response_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No response details found")

        return db_response_details

    # 특정 response의 모든 response_detail 조회
    @staticmethod
    async def get_all_response_details_by_response_id(response_id: int, db: AsyncSession):
        result = await db.execute(select(ResponseDetail).where(ResponseDetail.response_id == response_id))
        db_response_details = result.scalars().all()

        if not db_response_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No response details found")

        return db_response_details

    # 특정 response_detail 삭제
    @staticmethod
    async def delete_response_detail(response_detail_id: int, db: AsyncSession):
        db_response_detail = await db.execute(select(ResponseDetail).where(ResponseDetail.id == response_detail_id))
        deleted_response_detail = db_response_detail.scalar_one_or_none()
        if not deleted_response_detail:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ResponseDetail not found")

        await db.delete(deleted_response_detail)
        await db.commit()
        return {"msg": "ResponseDetail deleted", "deleted response_detail_id": response_detail_id}
