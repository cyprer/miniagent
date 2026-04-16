import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.messages import AIMessageChunk
import datetime
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

model = ChatAnthropic(
    model="MiniMax-M2.7",
    temperature=0,
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    thinking={"type": "enabled", "budget_tokens": 5000},
)

checkpointer = InMemorySaver()

@tool
def get_current_time() -> str:
    """获取当前系统时间，格式为YYYY-MM-DD HH:MM:SS"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

web_search = DuckDuckGoSearchRun(name="web_search", description="搜索互联网获取最新信息，当你需要查询实时新闻、天气预报、股票价格、实时比赛结果或其他最新数据时使用此工具")

SYSTEM_PROMPT = """你是一个智能助手。每次调用 web_search 搜索工具之前，**必须先调用 get_current_time 工具获取当前时间**，只有知道当前时间才能提供准确的信息。

重要规则：
- 调用 web_search 之前，先调用 get_current_time
- 返回结果时你应该标注信息的来源以及发布时间
- 遇到你不确定的信息你应该告知用户或者你需要用户提供一些信息你应该及时询问
"""

agent = create_agent(model, tools=[get_current_time, web_search], checkpointer=checkpointer, system_prompt=SYSTEM_PROMPT)

print("对话已启动（输入 exit/quit/q 退出）:\n")
config = {"configurable": {"thread_id": "1"}}
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
