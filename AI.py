from openai import OpenAI

from AI_config import KEY
from vector_db import get_collection, get_3_similar_document

client = OpenAI(api_key=KEY)


def ask_gpt(query: str, company_info: str):
    msg = [{"role": "assistant", "content": "You are a chatbot assistant for a company called Pionnet(파이언넷)."},
           {"role": "assistant", "content": "Read the [company info] and then respond to the question concisely."},
           {"role": "assistant", "content": "Do not assume; answer only with what you know."},
           {"role": "assistant", "content": f"[company info]\n{company_info}"},
           {"role": "user", "content": query}
           ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=msg
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    # 챗봇에게 파이언넷 관련해서 물어보는 코드
    query = "파이언넷 교통편"

    collection = get_collection("pionworld_data")
    company_info = get_3_similar_document(collection, query)
    completion = ask_gpt(query, company_info)

    print(f"질문: \"{query}\"")
    print(f"챗봇 답변:{completion}")
