from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List
from backend.app.database.models.email_logs import EmailLog
from backend.app.database.schemas.email_logs import (EmailLogsCreate, EmailLogsBulkCreate, EmailLogsRead)

# 이메일 로그 생성
async def create_email_log(db: AsyncSession, email_log: EmailLogsCreate) -> EmailLogsRead:
    db_email_log = EmailLog(**email_log.model_dump())
    db.add(db_email_log)
    await db.commit()
    await db.refresh(db_email_log)
    return EmailLogsRead.model_validate(db_email_log)

# 다중 이메일 로그 일괄 생성
async def create_bulk_email_logs(db: AsyncSession, bulk_data: EmailLogsBulkCreate) -> List[EmailLogsRead]:
    email_logs = [] # db.add() 작업이 완료된 이메일 로그를 저장할 배열
    
    # 각 수신자별로 개별 로그 생성
    for recipient in bulk_data.recipient_email:
        db_email_log = EmailLog(recipient_email=recipient, title=bulk_data.title, content=bulk_data.content, survey_id=bulk_data.survey_id)
        db.add(db_email_log)
        email_logs.append(db_email_log) # 추가된 이메일 로그는 email_logs 배열에 저장

    # 추가된 db_email_log 모두 commit
    await db.commit()
    
    # 각 로그를 새로고침하여 생성된 id와 created_at 가져오기 -> db에 insert함으로써 id, created_at값 생성
    for log in email_logs:
        await db.refresh(log)
    
    return [EmailLogsRead.model_validate(log) for log in email_logs]

# 특정 설문지의 이메일 로그 모두 조회
async def get_email_logs_by_survey_id(db: AsyncSession, survey_id: int) -> List[EmailLogsRead]:
    result = await db.execute(select(EmailLog).where(EmailLog.survey_id == survey_id))
    logs = result.scalars().all()
    return [EmailLogsRead.model_validate(log) for log in logs]

# 특정 이메일 로그 조회
async def get_email_log_by_id(db: AsyncSession, log_id: int) -> EmailLogsRead | None:
    result = await db.execute(select(EmailLog).where(EmailLog.id == log_id))
    log = result.scalar_one_or_none()
    return EmailLogsRead.model_validate(log) if log else None

# 특정 이메일 로그 삭제
async def delete_email_log(db: AsyncSession, log_id: int) -> bool:
    result = await db.execute(delete(EmailLog).where(EmailLog.id == log_id))
    await db.commit()
    return result.rowcount > 0

# 모든 이메일 로그 조회
async def get_all_email_logs(db: AsyncSession) -> List[EmailLogsRead]:
    result = await db.execute(select(EmailLog))
    logs = result.scalars().all()
    return [EmailLogsRead.model_validate(log) for log in logs]
