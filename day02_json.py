import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL") or None
)

model = os.getenv("MODEL")
SYSTEM_PROMPT = """你是一个信息提取助手。
用户会给你一段文本，你必须只输出 JSON，不要 markdown，不要解释。
JSON 格式：
{"answer": "一句话总结", "keywords": ["关键词1", "关键词2", "关键词3"]}
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def extract_info(text: str) -> dict:
    messages.append({"role": "user", "content": text})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
    )

    answer = response.choices[0].message.content.strip()
    try:
        result = json.loads(answer)
    except json.JSONDecodeError:
        result = {"answer": "无法解析的响应", "keywords": []}

    return result


if __name__ == "__main__":
    text_input = input("请输入文本进行信息提取：")
    result = extract_info(text_input)
    print("\n提取结果:")
    print(result)
    print("\nJSON 格式:", result.get("keywords", []))
