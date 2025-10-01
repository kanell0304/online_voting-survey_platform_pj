import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import asyncio
from typing import List, Tuple, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.models.email_logs import EmailLog
from backend.app.database.crud import email_crud


class EmailService:
    
    def __init__(self):
        self.sender_email = os.getenv("GMAIL_USER")
        self.app_password = os.getenv("GMAIL_APP_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        
    def validate_credentials(self) -> Tuple[bool, str]:
        if not self.sender_email:
            return False, "GMAIL_USER 환경 변수가 설정되지 않았습니다."
        if not self.app_password:
            return False, "GMAIL_APP_PASSWORD 환경 변수가 설정되지 않았습니다."
        return True, "인증 정보가 정상적으로 설정되었습니다."
    
    def create_survey_email_html(
        self, 
        survey_link: str,
        title: str,
        content: str
    ) -> str:
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Malgun Gothic', '맑은 고딕', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f9f9f9;
                }}
                .content {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h2 {{
                    color: #2c3e50;
                    margin-bottom: 20px;
                }}
                .message {{
                    margin: 20px 0;
                    padding: 15px;
                    background-color: #f8f9fa;
                    border-left: 4px solid #4CAF50;
                }}
                .button {{
                    display: inline-block;
                    padding: 14px 35px;
                    margin: 25px 0;
                    background-color: #4CAF50;
                    color: white !important;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 16px;
                }}
                .button:hover {{
                    background-color: #45a049;
                }}
                .link-section {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #f1f1f1;
                    border-radius: 5px;
                }}
                .link-section p {{
                    font-size: 13px;
                    color: #666;
                    margin: 5px 0;
                }}
                .link-section a {{
                    color: #4CAF50;
                    word-break: break-all;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    font-size: 12px;
                    color: #999;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h2>{title}</h2>
                    
                    <div class="message">
                        <p>{content}</p>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="{survey_link}" class="button">설문 참여하기</a>
                    </div>
                    
                    <div class="link-section">
                        <p>버튼이 작동하지 않는 경우, 아래 링크를 복사하여 브라우저에 붙여넣으세요:</p>
                        <a href="{survey_link}">{survey_link}</a>
                    </div>
                    
                    <div class="footer">
                        <p>본 메일은 발신 전용입니다.</p>
                        <p>© 2025 Survey Platform. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def create_email_message(
        self,
        recipient_email: str,
        title: str,
        content: str,
        survey_link: str
    ) -> MIMEMultipart:
        message = MIMEMultipart("alternative")
        message["Subject"] = title
        message["From"] = self.sender_email
        message["To"] = recipient_email

        html = self.create_survey_email_html(survey_link, title, content)

        text = f"""
{title}

{content}

아래 링크를 클릭하여 설문에 참여해주세요:
{survey_link}

감사합니다.
        """
        
        part1 = MIMEText(text, "plain", "utf-8")
        part2 = MIMEText(html, "html", "utf-8")
        
        message.attach(part1)
        message.attach(part2)
        
        return message
    
    async def send_single_email(
        self,
        recipient_email: str,
        title: str,
        content: str,
        survey_link: str
    ) -> Tuple[bool, str]:
        try:
            # 인증 정보 검증
            is_valid, msg = self.validate_credentials()
            if not is_valid:
                return False, msg
            
            message = self.create_email_message(
                recipient_email, title, content, survey_link
            )

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._send_email_sync,
                recipient_email,
                message.as_string()
            )
            
            return True, "이메일이 성공적으로 발송되었습니다."
        
        except smtplib.SMTPAuthenticationError:
            return False, "Gmail 인증 실패: 이메일 또는 앱 비밀번호를 확인하세요."
        except smtplib.SMTPRecipientsRefused:
            return False, f"수신자 이메일이 거부되었습니다: {recipient_email}"
        except smtplib.SMTPException as e:
            return False, f"SMTP 오류: {str(e)}"
        except Exception as e:
            return False, f"이메일 발송 실패: {str(e)}"
    
    def _send_email_sync(self, recipient_email: str, message_string: str):
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.sender_email, self.app_password)
            server.sendmail(self.sender_email, recipient_email, message_string)
    
    async def send_bulk_emails(
        self,
        email_logs: List[EmailLog],
        survey_id: int
    ) -> Dict[str, any]:
        
        survey_link = f"{self.frontend_url}/survey/{survey_id}"
        
        results = {
            "total": len(email_logs),
            "success_count": 0,
            "failed_count": 0,
            "success_emails": [],
            "failed_emails": []
        }

        tasks = []
        for log in email_logs:
            task = self.send_single_email(
                recipient_email=log.received_email,
                title=log.title,
                content=log.content,
                survey_link=survey_link
            )
            tasks.append((log.received_email, task))
        
        # 모든 작업을 동시에 실행
        for email, task in tasks:
            success, error_msg = await task
            
            if success:
                results["success_count"] += 1
                results["success_emails"].append(email)
            else:
                results["failed_count"] += 1
                results["failed_emails"].append({
                    "email": email,
                    "error": error_msg
                })
        
        return results
    
    async def send_from_email_logs(
        self,
        db: AsyncSession,
        survey_id: int
    ) -> Dict[str, any]:

        email_logs = await email_crud.get_email_logs_by_survey(db, survey_id)
        
        if not email_logs:
            return {
                "total": 0,
                "success_count": 0,
                "failed_count": 0,
                "message": "발송할 이메일이 없습니다."
            }
        
        # 이메일 발송
        results = await self.send_bulk_emails(email_logs, survey_id)
        results["survey_link"] = f"{self.frontend_url}/survey/{survey_id}"
        
        return results


# 싱글톤 인스턴스
email_service = EmailService()
