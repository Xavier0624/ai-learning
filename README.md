## 1. 单会话
```
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "你是一个简洁的助手。"},
        {"role": "user", "content": "你好，请用一句话介绍你自己。"},
    ],
    temperature=0.7,
    max_tokens=200,
)

print(response.choices[0].message.content)
```
`role`一般有三种值:
1. `system`表示角色设定
2. `user`用户输入
3. `assistant`模型之前的回答

`client.chat.completions.create`创建聊天补齐请求

`temperature`表示稳定性，越低越稳定
1. 问：用一句话解释什么是 API。
2. `temperature`为0时：API 是软件之间按约定规则交换数据和功能的接口
3. `temperature`1.2时：API（应用程序编程接口）是软件之间约定好的一套交互规则，让一个程序无需了解内部实现，就能调用另一个程序的功能或数据。

`max_tokens`生成的答复最大tokens

## 2. 多会话
```
while True:
    user_input = input("\n你:")
    if user_input.lower() == 'exit':
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )

    answer = response.choices[0].message.content
    print(f"\nAI: {answer}")

    messages.append({"role": "assistant", "content": answer})
```

`message.append()`附加内容

