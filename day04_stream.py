import os
import time
from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError, APITimeoutError

# load env
load_dotenv()

client = OpenAI(
    api_key = os.getenv("API_KEY"),
    base_url = os.getenv("BASE_URL") or None,
    timeout = 30,
    max_retries = 0,
)

model = os.getenv("MODEL")

SYSTEM_PROMPT = "你是一个软件工程学习助手。回答简洁，必要时给代码示例。"

# streaming response
def stream_chat(messages, max_retries = 3):
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model = model,
                messages = messages,
                stream = True,
                max_tokens = 1024,
                temperature = 0.7,
                stream_options = {"include_usage": True}
            )

            full_text_parts = []
            usage = None

            print("\nAI: ", end="", flush=True)

            for chunk in response:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    content = delta.content
                    if content:
                        print(content, end="", flush=True)
                        full_text_parts.append(content)

                if getattr(chunk, "usage", None):
                    usage = chunk.usage
            print()

            return "".join(full_text_parts), usage
        except (APIError, RateLimitError, APITimeoutError) as e:
            last_error = e
            wait = 2 * attempt
            print(f"\n[request error] 第 {attempt} 次：{e}")
            if attempt < max_retries:
                print(f"等待 {wait} 秒后重试...")
                time.sleep(wait)
        except Exception as e:
            last_error = e
            print(f"\n[unexpected error] {e}")
            break 
    print(f"\n[failed] 请求失败，错误信息：{last_error}")
    return "", None


def main():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        messages.append({"role": "user", "content": user_input})

        response_text, usage = stream_chat(messages)

        if not response_text:
            messages.pop()  # Remove the last user message if no response
            continue


        messages.append({"role": "assistant", "content": response_text})
        if usage:
            print(
                f"[tokens] prompt={usage.prompt_tokens}, "
                f"completion={usage.completion_tokens}, "
                f"total={usage.total_tokens}"
            )
        else:
            print("\n[Error] No response received.")


if __name__ == "__main__":
    main()