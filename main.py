from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from AI import ask_gpt
import crawler

import uvicorn

# FastAPI 기본 설정 (어디 보여지는 내용은 아님)
from vector_db import get_collection, get_3_similar_document

app = FastAPI(
    description="똑똑한 파이언월드 챗봇",
    title="Smart Pionworld Chatbot"
)

# 접속 허용하는 url 정의
# 이 설정이 없으면 로컬로 돌릴 때 파일이 안 뜰 수 있음
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# swagger api 문서를 꾸미기 위한 설정
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Smart Pionworld Chatbot",
        version="1.0.0",
        description="똑똑한 파이언월드 챗봇",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.mount("/assets", StaticFiles(directory="assets"))  # FileResponse에서 index.html을 띄우는데 필요한 assets
app.mount("/", StaticFiles(directory="pages", html=True))  # html 파일 경로 리턴

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

"""
    파이언월드 크롤링 api
    텍스트를 파일 형태로 저장
    :return: 파이언월드 사이트전문 text
"""


@app.get("/pionworld",
         tags=["API"],
         response_class=PlainTextResponse)
async def get_text_from_pion_world():
    return crawler.scrap_pion_world()


"""
    파이언월드 챗봇 api, index.html에서 호출중.
    :param: query 유저 질문
    :return: 챗봇 답변
"""


@app.get("/chatbot",
         tags=["API"])
async def chatbot(query: str):
    collection = get_collection('pionworld_data')
    company_info = get_3_similar_document(collection, query)
    answer = ask_gpt(query, company_info)
    return f'🤖 {answer}'
