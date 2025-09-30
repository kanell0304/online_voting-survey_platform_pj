1. 불러오기
git clone 링크 .

2. develop브랜치 가져오기
git checkout -b develop origin/develop

3. npm 세팅
cd frontend (꼭 frontend들어가서 npm install하기)
npm install
npm list

4. 첫 작업
git add .
git commit -m "작업 내용 간단히 작성"
git push -u origin develop

-------------------------------------------------
terminal로 backend 폴더로 이동 후 다음을 순서대로 실행

1. echo "DATABASE_URL=mysql+pymysql://root:1234@localhost:3306/fastapi_db?charset=utf8mb4" > .env

2. 'root:1234' 부분을 본인의 DB상황에 맞게 수정

3. 가상환경 실행 후 가상 환경(cmd)에서 다음명령어를 실행 # 실행 경로: (프로젝트 파일)/backend

pip install -r requirements.txt



4.