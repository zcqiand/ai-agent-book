# 传统方式：集中式路由
def handle_request(user_input):
    intent = classify_intent(user_input)

    if intent == "tech":
        result = tech_agent.run(user_input)
    elif intent == "billing":
        result = billing_agent.run(user_input)
    elif intent == "complaint":
        result = complaint_agent.run(user_input)

    return result
