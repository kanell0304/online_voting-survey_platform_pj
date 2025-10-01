from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backend.app.database.database import get_db
from backend.app.database.schemas.email_logs import (
    EmailLogsCreate,
    EmailLogsBulkCreate,
    EmailLogsRead,
    EmailSendResponse,
    EmailTestRequest
)
from backend.app.database.crud import email_crud
from backend.app.service.email_service import email_service
import os

router = APIRouter(
    prefix="/emails",
    tags=["Email Management"]
)


@router.get("/config")
async def check_email_config():
    """이메일 설정 확인"""
    return {
        "gmail_user": os.getenv("GMAIL_USER", "설정 안됨"),
        "app_password_set": bool(os.getenv("GMAIL_APP_PASSWORD")),
        "frontend_url": os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 465
    }


@router.post("/test", response_model=dict)
async def send_test_email(test_request: EmailTestRequest):
    """테스트 이메일 발송 (비동기)"""
    survey_link = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/survey/{test_request.survey_id}"
    
    success, message = await email_service.send_single_email(
        recipient_email=test_request.recipient,
        title=test_request.title,
        content=test_request.content,
        survey_link=survey_link
    )
    
    if not success:
        raise HTTPException(status_code=500, detail=message)
    
    return {
        "success": True,
        "message": message,
        "recipient": test_request.recipient,
        "survey_link": survey_link
    }


@router.post("/logs", response_model=EmailLogsRead)
async def create_email_log(
    email_log: EmailLogsCreate,
    db: AsyncSession = Depends(get_db)
):
    """단일 이메일 로그 생성 (비동기)"""
    return await email_crud.create_email_log(db, email_log)


@router.post("/logs/bulk", response_model=List[EmailLogsRead])
async def create_bulk_email_logs(
    bulk_data: EmailLogsBulkCreate,
    db: AsyncSession = Depends(get_db)
):
    """여러 이메일 로그 일괄 생성 (비동기)"""
    return await email_crud.create_bulk_email_logs(db, bulk_data)


@router.get("/logs/survey/{survey_id}", response_model=List[EmailLogsRead])
async def get_email_logs_by_survey(
    survey_id: int,
    db: AsyncSession = Depends(get_db)
):
    """특정 설문지의 이메일 로그 조회 (비동기)"""
    logs = await email_crud.get_email_logs_by_survey(db, survey_id)
    if not logs:
        raise HTTPException(status_code=404, detail="해당 설문지의 이메일 로그가 없습니다.")
    return logs


@router.get("/logs/{log_id}", response_model=EmailLogsRead)
async def get_email_log(
    log_id: int,
    db: AsyncSession = Depends(get_db)
):
    """ID로 이메일 로그 조회 (비동기)"""
    log = await email_crud.get_email_log_by_id(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="이메일 로그를 찾을 수 없습니다.")
    return log


@router.delete("/logs/{log_id}")
async def delete_email_log(
    log_id: int,
    db: AsyncSession = Depends(get_db)
):
    """이메일 로그 삭제 (비동기)"""
    success = await email_crud.delete_email_log(db, log_id)
    if not success:
        raise HTTPException(status_code=404, detail="이메일 로그를 찾을 수 없습니다.")
    return {"message": "이메일 로그가 삭제되었습니다."}


@router.post("/send/survey/{survey_id}", response_model=EmailSendResponse)
async def send_survey_emails(
    survey_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    설문지 이메일 발송 (email_logs 테이블 기반, 비동기 백그라운드)
    
    - survey_id에 해당하는 모든 email_logs를 조회
    - 각 로그의 받는 사람에게 이메일 발송
    - 백그라운드에서 처리
    """
    
    # email_logs 조회
    email_logs = await email_crud.get_email_logs_by_survey(db, survey_id)
    
    if not email_logs:
        raise HTTPException(
            status_code=404,
            detail=f"설문지 ID {survey_id}에 대한 이메일 로그가 없습니다."
        )
    
    # Gmail 발송 제한 체크 (하루 500통)
    if len(email_logs) > 500:
        raise HTTPException(
            status_code=400,
            detail=f"Gmail은 하루 500통까지만 발송 가능합니다. (현재: {len(email_logs)}통)"
        )
    
    # 백그라운드에서 이메일 발송
    async def send_emails_task():
        await email_service.send_bulk_emails(email_logs, survey_id)
    
    background_tasks.add_task(send_emails_task)
    
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    survey_link = f"{frontend_url}/survey/{survey_id}"
    
    return EmailSendResponse(
        total=len(email_logs),
        success_count=0,  # 백그라운드 작업이므로 0
        failed_count=0,
        survey_link=survey_link,
        success_emails=[],
        failed_emails=[]
    )


@router.post("/send/survey/{survey_id}/sync", response_model=EmailSendResponse)
async def send_survey_emails_sync(
    survey_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    설문지 이메일 동기 발송 (결과 즉시 반환, 비동기)
    
    - 백그라운드가 아닌 즉시 처리
    - 발송 결과를 바로 확인 가능
    """
    results = await email_service.send_from_email_logs(db, survey_id)
    
    if results.get("total", 0) == 0:
        raise HTTPException(
            status_code=404,
            detail="발송할 이메일이 없습니다."
        )
    
    return EmailSendResponse(**results)


@router.post("/create-and-send", response_model=dict)
async def create_and_send_emails(
    bulk_data: EmailLogsBulkCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    이메일 로그 생성 후 즉시 발송 (비동기)
    
    1. email_logs 테이블에 데이터 저장
    2. 저장된 데이터로 이메일 발송
    """
    
    # 1. email_logs에 저장
    email_logs = await email_crud.create_bulk_email_logs(db, bulk_data)
    
    # 2. 이메일 발송 (백그라운드)
    async def send_emails_task():
        await email_service.send_bulk_emails(email_logs, bulk_data.survey_id)
    
    background_tasks.add_task(send_emails_task)
    
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    survey_link = f"{frontend_url}/survey/{bulk_data.survey_id}"
    
    return {
        "message": f"{len(bulk_data.recipients)}명에게 이메일 발송이 시작되었습니다.",
        "total": len(bulk_data.recipients),
        "survey_link": survey_link,
        "created_logs": len(email_logs)
    }
