import os
import json
import ast
import operator

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL") or None
)
model = os.getenv("MODEL")

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def safe_eval(node):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    raise ValueError("不支持的表达式")

def calculator(expression: str) -> dict:
    try:
        tree = ast.parse(expression, mode='eval')
        result = safe_eval(tree)
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"expression": expression, "error": str(e)}


def get_weather(city: str) -> dict:
    fake = {
        "北京": {"temperature": 20, "humidity": 60},
        "上海": {"temperature": 25, "humidity": 70},
        "广州": {"temperature": 30, "humidity": 80}
    }
    data = fake.get(city)
    if not data:
        return {"city": city, "error": "城市数据不可用"}
    return {"city": city, "temperature": data["temperature"], "humidity": data["humidity"]}


tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式的结果",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询城市天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "要查询的城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

TOOL_MAP = {
    "calculator": calculator,
    "get_weather": get_weather
}

messages = [
    {"role": "system", "content": "你是一个多功能助手。你可以执行数学计算和查询城市天气信息。用户会给你一个请求，你必须根据请求调用相应的工具，并返回结果。请确保只输出 JSON 格式的响应，不要包含任何解释或额外文本。"}
]

while True:
    user_input = input("请输入请求（或输入 'exit' 退出）：")
    if user_input.lower() == 'exit':
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        tools=tools,
        tool_choice="auto"
    )

    assistant_msg = response.choices[0].message

    if not assistant_msg.tool_calls:
        print(f"AI: {assistant_msg.content}")
        messages.append({"role": "assistant", "content": assistant_msg.content})
        continue

    messages.append({"role": "assistant", "content": assistant_msg.content, "tool_calls": assistant_msg.tool_calls})

    for tool_call in assistant_msg.tool_calls:
        tool_name = tool_call.function.name
        tool_args = tool_call.function.arguments

        print(f"\n[模型请求调用] {tool_name}({tool_args})")


        try:
            args = json.loads(tool_args)
        except json.JSONDecodeError:
            args = {}
            result = {"error": f"无法解析的工具参数: {tool_args}"}
        else:
            tool_func = TOOL_MAP.get(tool_name)
            if tool_func:
                result = tool_func(**args)
            else:
                result = {"error": f"未知的工具: {tool_name}"}

        

        print(f"工具调用结果: {json.dumps(result, ensure_ascii=False)}")

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result, ensure_ascii=False)
        })

    final_response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        tool_choice="auto",
        tools=tools
    )

    final_msg = final_response.choices[0].message
    print(f"\nAI 最终响应: {final_msg.content}")
    messages.append({"role": "assistant", "content": final_msg.content})
