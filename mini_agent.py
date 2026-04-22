import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.messages import AIMessageChunk

from tools import get_tools

load_dotenv()

model = ChatAnthropic(
    model="MiniMax-M2.7",
    temperature=0,
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    thinking={"type": "enabled", "budget_tokens": 5000},
)

checkpointer = InMemorySaver()

SYSTEM_PROMPT = """你是一个智能助手。

重要规则：
- 只有在需要使用 web_search 获取实时信息时，才先调用 get_current_time 获取当前时间；普通对话或问候不需要获取时间
- 调用 web_search 之前，先调用 get_current_time
- 返回结果时你应该标注信息的来源以及发布时间
- 遇到你不确定的信息你应该告知用户或者你需要用户提供一些信息你应该及时询问
"""

agent = create_agent(model, tools=get_tools(), checkpointer=checkpointer, system_prompt=SYSTEM_PROMPT)

if __name__ == "__main__":
    print("对话已启动（输入 exit/quit/q 退出）:\n")
    config = {"configurable": {"thread_id": "1"}}
    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in ["exit", "quit", "q", "退出"]:
            print("再见!")
            break

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
