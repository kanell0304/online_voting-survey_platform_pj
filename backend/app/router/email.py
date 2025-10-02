from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.app.database.database import get_db
from backend.app.database.schemas.email_logs import (EmailLogsCreate, EmailLogsBulkCreate, EmailLogsRead, EmailSendResponse, EmailTestRequest)
from backend.app.database.crud import email_crud
from backend.app.service.email_service import email_service
import os

router = APIRouter(prefix="/emails", tags=["Email Logs"])

# 테스트 이메일 발송
@router.post("/test", response_model=dict)
async def send_test_email(test_request: EmailTestRequest):
    survey_link = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/survey/{test_request.survey_id}" # 설문지 링크
    
    is_success, message = await email_service.send_single_email(recipient_email=test_request.recipient, title=test_request.title, content=test_request.content, survey_link=survey_link)
    
    if not is_success: # 실패했다면
        raise HTTPException(status_code=500, detail=message)
    
    return {"성공 여부": True, "msg": message, "받는사람": test_request.recipient, "설문지 링크": survey_link}

# 단일 이메일 로그 생성
@router.post("/logs", response_model=EmailLogsRead)
async def create_email_log(email_log: EmailLogsCreate, db: AsyncSession = Depends(get_db)):
    result = await email_crud.create_email_log(db, email_log)
    return result

# 이메일 로그 다중 생성
@router.post("/logs/bulk", response_model=List[EmailLogsRead])
async def create_bulk_email_logs(bulk_data: EmailLogsBulkCreate, db: AsyncSession = Depends(get_db)):
    result = await email_crud.create_bulk_email_logs(db, bulk_data)
    return result

# 특정 설문지의 이메일 로그 조회
@router.get("/logs/survey/{survey_id}", response_model=List[EmailLogsRead])
async def get_email_logs_by_survey_id(survey_id: int, db: AsyncSession = Depends(get_db)):
    results = await email_crud.get_email_logs_by_survey_id(db, survey_id)
    if results is None:
        raise HTTPException(status_code=404, detail="Email Log Not Found")
    return results

# 특정 이메일 로그 조회
@router.get("/logs/{log_id}", response_model=EmailLogsRead)
async def get_email_log_by_id(log_id: int, db: AsyncSession = Depends(get_db)):
    result = await email_crud.get_email_log_by_id(db, log_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Email Log Not Found")
    return result

# 특정 이메일 로그 삭제
@router.delete("/logs/{log_id}")
async def delete_email_log_by_id(log_id: int, db: AsyncSession = Depends(get_db)):
    success = await email_crud.delete_email_log(db, log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Email Log Not Found")
    return {"msg": "Delete Success Email Log"}


# 설문지 이메일 발송
@router.post("/send/survey/{survey_id}", response_model=EmailSendResponse)
async def send_survey_emails(survey_id: int, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    email_logs = await email_crud.get_email_logs_by_survey_id(db, survey_id)
    
    if email_logs is None: # survey_id에 해당하는 이메일 로그가 없다면
        raise HTTPException(status_code=404, detail=f"Email Log Not Found by survey_id: {survey_id}")
    
    # gmail 발송 제한 체크 (하루 500통만 가능)
    if len(email_logs) > 500:
        raise HTTPException(status_code=400, detail=f"Gmail은 하루 500통까지만 발송 가능합니다. (현재: {len(email_logs)}통)")
    
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

# 이메일 발송 - 로그를 DB에 저장 후 이메일 발송
@router.post("/create-and-send", response_model=dict)
async def create_and_send_emails(bulk_data: EmailLogsBulkCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    # 1. email_logs에 저장
    email_logs = await email_crud.create_bulk_email_logs(db, bulk_data)
    
    # 2. 이메일 발송 (background)
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
