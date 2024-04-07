from pydantic import BaseModel

"""
    모델 예시.
    input output을 모두 plain text로 주고받을 경우 안 싸도 ok
"""

class ChatBotReply(BaseModel):
    content: str

class ChatBotQuery(BaseModel):
    content: str
    user: str