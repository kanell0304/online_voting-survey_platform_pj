from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.database.models.email_logs import EmailLog
from backend.app.database.schemas.email_logs import EmailLogsCreate, EmailLogsBulkCreate
from typing import List


async def create_email_log(db: AsyncSession, email_log: EmailLogsCreate) -> EmailLog:
    db_email_log = EmailLog(
        received_email=email_log.received_email,
        title=email_log.title,
        content=email_log.content,
        survey_id=email_log.survey_id
    )
    db.add(db_email_log)
    await db.commit()
    await db.refresh(db_email_log)
    return db_email_log


async def create_bulk_email_logs(db: AsyncSession, bulk_data: EmailLogsBulkCreate) -> List[EmailLog]:
    email_logs = []
    
    for recipient in bulk_data.recipients:
        db_email_log = EmailLog(
            received_email=recipient,
            title=bulk_data.title,
            content=bulk_data.content,
            survey_id=bulk_data.survey_id
        )
        email_logs.append(db_email_log)
    
    db.add_all(email_logs)
    await db.commit()
    
    # 생성된 객체들 refresh
    for log in email_logs:
        await db.refresh(log)
    
    return email_logs


async def get_email_logs_by_survey(db: AsyncSession, survey_id: int) -> List[EmailLog]:
    result = await db.execute(
        select(EmailLog).filter(EmailLog.survey_id == survey_id)
    )
    return result.scalars().all()


async def get_email_log_by_id(db: AsyncSession, log_id: int) -> EmailLog:
    result = await db.execute(
        select(EmailLog).filter(EmailLog.id == log_id)
    )
    return result.scalar_one_or_none()


async def delete_email_log(db: AsyncSession, log_id: int) -> bool:
    email_log = await get_email_log_by_id(db, log_id)
    if email_log:
        await db.delete(email_log)
        await db.commit()
        return True
    return False
