import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key = os.getenv("API_KEY"),
    base_url = os.getenv("BASE_URL"),
)
model = os.getenv("MODEL")

messages=[
    {"role": "system", "content": "你是一个简洁的助手。"},
]

while True:
    user_input = input("\n你:")
    if user_input.lower() == 'exit':
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=2.0,
        max_tokens=500,
    )

    answer = response.choices[0].message.content
    print(f"\nAI: {answer}")

    messages.append({"role": "assistant", "content": answer})
