# 传统方式：硬编码路由
if intent == "tech":
    response = tech_agent.run(user_input)
elif intent == "billing":
    response = billing_agent.run(user_input)
