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

## 3. git
`git commit -m ""`添加提交

`git remote -M main"` `git remote` 表示操作远程仓库 `-m -M`报错/不报错 重命名

`git remote add origin 仓库地址` `origin`是仓库地址的别名

`git push -u(--set-upstream) origin main` `-u`表示设置上游分支 初次时使用


## 常见报错

| 报错 | 原因 | 解决 |
|---|---|---|
| `401 Unauthorized` | Key 错或 `.env` 没加载 | 检查 `.env` 和变量名 |
| `404 model not found` | `BASE_URL` 或 `MODEL` 不对 | 核对平台文档 |
| `429` | 余额不足/限流 | 换 key 或稍后再试 |
| `Connection error` | 网络/代理 | 检查网络 |
| `ModuleNotFoundError` | 没激活虚拟环境 | 重新 activate |