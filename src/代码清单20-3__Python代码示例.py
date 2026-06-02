
# 当 Agent 运行时，内部发生：

# 1. 输入消息被组装
input_messages = [
    {"role": "system", "content": instructions},
    {"role": "user", "content": user_input}
]

# 2. LLM 生成响应
llm_response = llm.generate(input_messages, tools)

# 3. 如果有工具调用，执行工具
if llm_response.tool_calls:
    for call in llm_response.tool_calls:
        result = execute_tool(call)
        input_messages.append(llm_response)
        input_messages.append({"role": "tool", "content": result})

# 4. 重复直到 LLM 不再调用工具
# 5. 返回最终文本响应

## 20.4　Handoffs 原理详解

### Handoffs 的本质

Handoffs 是 OpenAI Agents SDK 最独特的设计——它允许一个 Agent 将**控制权**和**上下文**完整地移交给另一个 Agent。 <!-- src:kp-003-01,src-003 -->

在传统实现中，多角色协作通常这样写：