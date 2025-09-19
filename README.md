1. 불러오기
git clone 링크 .

2. dev브랜치 가져오기
git switch -c dev origin/dev
git switch dev
git pull origin dev

3. 개별 브랜치 만들기
git switch -c 브랜치이름

4. npm 세팅
cd frontend (꼭 frontend들어가서 npm install하기)
npm install
npm list

5. 첫 작업
git add .
git commit -m "작업 내용 간단히 작성"
git push -u origin tata

-------------------------------------------------
terminal로 backend 폴더로 이동 후 다음을 순서대로 실행

1. echo "DATABASE_URL=mysql+pymysql://root:1234@localhost:3306/fastapi_db?charset=utf8mb4" > .env

2. 'root:1234' 부분을 본인의 DB상황에 맞게 수정

3. 가상환경 실행 후 가상 환경(cmd)에서 다음을 실행 # 실행 경로: (프로젝트 파일)/backend

pip install -r requirements.txt