# """
# Gmail SMTP 이메일 발송 테스트 스크립트
#
# 사용법:
#     python test_email.py
# """
#
# import requests
# import json
#
# # 서버 URL
# BASE_URL = "http://localhost:8000/api/emails"
#
#
# def test_config():
#     """이메일 설정 확인"""
#     print("=" * 50)
#     print("1. 이메일 설정 확인")
#     print("=" * 50)
#
#     response = requests.get(f"{BASE_URL}/config")
#     print(json.dumps(response.json(), indent=2, ensure_ascii=False))
#     print()
#
#
# def test_single_email(recipient: str):
#     """테스트 이메일 발송"""
#     print("=" * 50)
#     print("2. 테스트 이메일 발송")
#     print("=" * 50)
#
#     data = {
#         "recipient": recipient,
#         "title": "테스트 이메일",
#         "content": "이것은 Gmail SMTP 테스트 이메일입니다.",
#         "survey_id": 1
#     }
#
#     response = requests.post(f"{BASE_URL}/test", json=data)
#
#     if response.status_code == 200:
#         print("테스트 이메일 발송 성공!")
#         print(json.dumps(response.json(), indent=2, ensure_ascii=False))
#     else:
#         print("테스트 이메일 발송 실패!")
#         print(response.text)
#     print()
#
#
# def test_bulk_create_and_send(survey_id: int, recipients: list):
#     """이메일 로그 생성 + 즉시 발송"""
#     print("=" * 50)
#     print("3. 이메일 로그 생성 + 발송")
#     print("=" * 50)
#
#     data = {
#         "survey_id": survey_id,
#         "title": "2025 고객 만족도 조사",
#         "content": "안녕하세요! 귀하의 소중한 의견을 듣고자 설문조사를 진행합니다. 5분만 투자하여 참여해주세요.",
#         "recipients": recipients
#     }
#
#     response = requests.post(f"{BASE_URL}/create-and-send", json=data)
#
#     if response.status_code == 200:
#         print("이메일 발송 시작!")
#         print(json.dumps(response.json(), indent=2, ensure_ascii=False))
#     else:
#         print("발송 실패!")
#         print(response.text)
#     print()
#
#
# def test_sync_send(survey_id: int):
#     """동기 발송 (결과 즉시 확인)"""
#     print("=" * 50)
#     print("4. 동기 발송 (결과 확인)")
#     print("=" * 50)
#
#     response = requests.post(f"{BASE_URL}/send/survey/{survey_id}/sync")
#
#     if response.status_code == 200:
#         result = response.json()
#         print("발송 완료!")
#         print(f"총: {result['total']}명")
#         print(f"성공: {result['success_count']}명")
#         print(f"실패: {result['failed_count']}명")
#         print(f"링크: {result['survey_link']}")
#
#         if result['failed_emails']:
#             print("\n실패한 이메일:")
#             for failed in result['failed_emails']:
#                 print(f"  - {failed['email']}: {failed['error']}")
#     else:
#         print("발송 실패!")
#         print(response.text)
#     print()
#
#
# def main():
#     """메인 테스트 실행"""
#     print("\n🚀 Gmail SMTP 이메일 발송 테스트 시작\n")
#
#     # 1. 설정 확인
#     test_config()
#
#     # 2. 테스트 이메일 발송 (자신의 이메일로 변경)
#     print("테스트 이메일을 받을 이메일 주소를 입력하세요:")
#     test_recipient = input("이메일: ").strip()
#
#     if test_recipient:
#         test_single_email(test_recipient)
#
#         # 추가 테스트 여부 확인
#         choice = input("\n이메일 로그 생성 + 발송 테스트를 진행하시겠습니까? (y/n): ").strip().lower()
#
#         if choice == 'y':
#             # 3. 이메일 로그 생성 + 발송
#             print("\n받는 사람 이메일을 쉼표로 구분하여 입력하세요:")
#             recipients_input = input("이메일들: ").strip()
#             recipients = [email.strip() for email in recipients_input.split(',')]
#
#             survey_id = int(input("설문지 ID (예: 1): ").strip() or "1")
#
#             test_bulk_create_and_send(survey_id, recipients)
#
#     print("\n테스트 완료!\n")
#
#
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\n테스트가 중단되었습니다.")
#     except Exception as e:
#         print(f"\n\n오류 발생: {str(e)}")
