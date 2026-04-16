import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.messages import AIMessageChunk
import datetime
from langchain.tools import tool

load_dotenv()

model = ChatAnthropic(
    model="MiniMax-M2.7",
    temperature=0,
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    thinking={"type": "enabled", "budget_tokens": 5000},
)

checkpointer = InMemorySaver()

# 定义获取当前系统时间的tool
@tool
def get_current_time() -> str:
    """获取当前系统时间，格式为YYYY-MM-DD HH:MM:SS"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

agent = create_agent(model, tools=[get_current_time], checkpointer=checkpointer)

print("对话已启动（输入 exit/quit/q 退出）:\n")
now = datetime.datetime.now()
config = {"configurable": {"thread_id": "1"}}
print(now.strftime("%Y-%m-%d %H:%M:%S"))
while True:
    user_input = input("你: ").strip()
    if user_input.lower() in ["exit", "quit", "q", "退出"]:
        print("再见!")
        break

    reasoning_text = ""
    answer_text = ""
    show_reasoning = False
    show_answer = False

    for token, metadata in agent.stream(
        {"messages": [("user", user_input)]},
        config,
        stream_mode="messages",
    ):
        if not isinstance(token, AIMessageChunk):
            continue

        reasoning = [b for b in token.content_blocks if b.get("type") in ("thinking", "reasoning")]
        text = [b for b in token.content_blocks if b.get("type") == "text"]

        if reasoning and not show_reasoning:
            print("🧠 思考: ", end="")
            show_reasoning = True
        if reasoning:
            print(f"{reasoning[0]['reasoning']}", end="")

        if text and not show_answer:
            print()
            print("💬 回答: ", end="")
            show_answer = True
        if text:
            print(text[0]["text"], end="")

    print()
