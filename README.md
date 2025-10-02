1. 불러오기 <br>
git clone 링크 .

2. develop브랜치 가져오기 <br>
git checkout -b develop origin/develop

3. npm 세팅 <br>
cd frontend (꼭 frontend들어가서 npm install하기) <br>
npm install <br>
npm list

4. 첫 작업 <br>
git add . <br>
git commit -m "작업 내용 간단히 작성" <br>
git push -u origin develop

-------------------------------------------------
terminal로 backend 폴더로 이동 후 다음을 순서대로 실행

1. echo "" > .env

2. .env에 다음 내용을 작성(br태그를 제외하고 입력) <br>
#DB 설정 <br>
DB_USER=root <br>
DB_PASSWORD=1234 <br>
DB_HOST=localhost <br>
DB_PORT=3306 <br>
DB_NAME=team_project_db <br>

#JWT 설정 <br>
SECRET_KEY=secretkeyfast <br>
JWT_ALGORITHM=HS256 <br>
ACCESS_TOKEN_EXPIRE=6000 <br>
REFRESH_TOKEN_EXPIRE=604800 <br>

#Gmail SMTP 설정 <br>
GMAIL_USER=tptestemail0930@gmail.com <br>
GMAIL_APP_PASSWORD=jcwd dfux gopx ryzz <br>
FRONTEND_URL=http://localhost:3000 <br>

3. DB_USER, DB_PASSWORD 부분을 자신의 DB 상환에 맞게 수정
4. 가상환경 실행 후 가상 환경(cmd)에서 다음명령어를 실행 # 실행 경로: (프로젝트 파일)/backend

pip install -r requirements.txt