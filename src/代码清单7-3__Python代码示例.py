from anthropic import Anthropic

client = Anthropic()

messages = []

# 第一轮
messages.append({"role": "user", "content": "我叫张三"})
response1 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages
)
messages.append({"role": "assistant", "content": response1.content[0].text})
print(f"第一轮: {response1.content[0].text}")

# 第二轮（带上下文）
messages.append({"role": "user", "content": "记住我叫什么了吗？"})
response2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages
)
print(f"第二轮: {response2.content[0].text}")