echo "파이언넷 챗봇 init을 시작합니다."

echo "프로젝트에 필요한 라이브러리를 설치합니다."
venv/bin/pip3.9 install -r requirements.txt

echo "크롤링을 시작합니다."
venv/bin/python3 crawler.py

echo "크로마DB 초기화를 시작합니다."
venv/bin/python3 vector_db.py