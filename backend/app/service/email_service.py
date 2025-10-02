import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from backend.app.database.schemas.email_logs import EmailLogsRead
from backend.app.database.crud import email_crud


class EmailService:
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.gmail_user = os.getenv("GMAIL_USER")
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD")
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # 이메일 폼 생성(title, content를 삽입하고 임시 css를 적용) - 향후 삭제 가능
    def _create_html_content(self, content: str, survey_link: str) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body{{font-family: Arial, sans-serif; line-height: 1.6; color: #333;}}
                .container{{max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;}}
                .content{{background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}}
                .button{{display: inline-block; padding: 12px 30px; margin: 20px 0; background-color: #4CAF50; color: white !important; text-decoration: none; border-radius: 5px; font-weight: bold;}}
                .button:hover{{background-color: #45a049;}}
                .footer{{margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; text-align: center;}}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h2>설문 요청</h2>
                    <p>{content}</p>
                    <p style="text-align: center;">
                        <a href="{survey_link}" class="button">설문 참여하기</a>
                    </p>
                    <p style="font-size: 14px; color: #666;">
                        또는 아래 링크를 복사하여 브라우저에 붙여넣으세요:<br>
                        <a href="{survey_link}">{survey_link}</a>
                    </p>
                </div>
                <div class="footer">
                    <p>본 이메일은 'Online Voting/Survey Platform'에서 자동으로 발송되었습니다.</p>
                    <p>문의사항이 있으시면 발신자({self.gmail_user})에게 회신해주세요.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    async def send_single_email(self,recipient_email: str, title: str, content: str, survey_link: str) -> Tuple[bool, str]:
        try:
            # MIME 메시지 생성
            msg = MIMEMultipart('alternative')
            msg['Subject'] = title
            msg['From'] = self.gmail_user
            msg['To'] = recipient_email
            
            # HTML 내용 생성
            html_content = self._create_html_content(content, survey_link)
            
            # HTML 파트 추가
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 동기 작업을 별도 스레드에서 실행
            def send_sync():
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    server.login(self.gmail_user, self.gmail_password)
                    server.send_message(msg)
            
            # 동기 함수를 비동기로 실행
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, send_sync)
            
            return True, f"{recipient_email}로 이메일 발송 성공" # 발송 성공 여부와 메세지 반환
            
        except smtplib.SMTPAuthenticationError:
            return False, "Gmail 인증 실패. GMAIL_USER와 GMAIL_APP_PASSWORD를 확인하세요."
        except smtplib.SMTPException as e:
            return False, f"SMTP 오류: {str(e)}"
        except Exception as e:
            return False, f"이메일 발송 실패 ({recipient_email}): {str(e)}"

    # 이메일 다중 일괄 발송
    async def send_bulk_emails(self, email_logs: List[EmailLogsRead], survey_id: int) -> Dict:
        total = len(email_logs) # 총 개수
        success_count = 0 # 발송 성공 개수
        failed_count = 0 # 발송 실패 개수
        success_emails = [] # 발송 성공한 이메일 정보 저장
        failed_emails = [] # 발송 실패한 이메일 정보 저장
        
        survey_link = f"{self.frontend_url}/survey/{survey_id}" # 설문지 링크: http://localhost:3000/survey/{survey_id}
        
        # 각 이메일을 순차적으로 발송 (Gmail 제한 고려)
        for log in email_logs:
            success, message = await self.send_single_email(recipient_email=log.recipient_email, title=log.title, content=log.content, survey_link=survey_link)

            # 성공/실패 여부 기록
            if success:
                success_count += 1
                success_emails.append(log.recipient_email)
                print(message)
            else:
                failed_count += 1
                failed_emails.append(log.recipient_email)
                print(message)

            await asyncio.sleep(0.1)  # gmail 발송 제한 방지를 위한 0.1초 대기
        
        return {
            "total": total, # 총 개수
            "success_count": success_count, # 발송 성공 개수
            "failed_count": failed_count, # 발송 실패 개수
            "survey_link": survey_link, # 설문지 링크
            "success_emails": success_emails, # 발송 성공 이메일 정보
            "failed_emails": failed_emails # 발송 실패 이메일 정보
        }

    # email_logs 테이블의 데이터를 기반으로 비동기 이메일 발송
    async def send_from_email_logs(self, db: AsyncSession, survey_id: int) -> Dict:
        email_logs = await email_crud.get_email_logs_by_survey_id(db, survey_id)
        
        if not email_logs:
            return {
                "total": 0,
                "success_count": 0,
                "failed_count": 0,
                "survey_link": "",
                "success_emails": [],
                "failed_emails": []
            }
        
        # 이메일 발송
        return await self.send_bulk_emails(email_logs, survey_id)

# 싱글톤 인스턴스 생성
email_service = EmailService()
