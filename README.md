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

1. echo "" > .env

2. .env에 다음 내용을 작성
3. 
#DB 설정
DB_USER=root
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=3306
DB_NAME=team_project_db

#JWT 설정
SECRET_KEY=secretkeyfast
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=6000
REFRESH_TOKEN_EXPIRE=604800

#Gmail SMTP 설정
GMAIL_USER=tptestemail0930@gmail.com
GMAIL_APP_PASSWORD=jcwd dfux gopx ryzz
FRONTEND_URL=http://localhost:3000

3. DB_USER, DB_PASSWORD 부분을 자신의 DB 상환에 맞게 수정

4. 가상환경 실행 후 가상 환경(cmd)에서 다음명령어를 실행 # 실행 경로: (프로젝트 파일)/backend

pip install -r requirements.txt