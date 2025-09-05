from Agent_ReAct import build_react_agent


if __name__ == "__main__":
    agent = build_react_agent()
    prompt = input("Nhập yêu cầu cho Agent: ")
    result = agent.invoke({"messages": [("user", prompt)]})
    print("Kết quả trả về:", result["messages"][-1].content)