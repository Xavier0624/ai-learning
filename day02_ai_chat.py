import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL") or None
)

model = os.getenv("MODEL")
SYSTEM_PROMPT = "你是一个软件工程学习助手。回答简洁，必要时给代码示例。"

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_input = input("\nUser:")

    if user_input.strip().lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
    )

    answer = response.choices[0].message.content
    print(f"\nAI: {answer}")

    messages.append({"role": "assistant", "content": answer})

