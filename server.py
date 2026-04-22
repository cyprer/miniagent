import os
import json
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from langchain.messages import AIMessageChunk

from mini_agent import agent

load_dotenv()

app = FastAPI(title="MiniAgent Web")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/chat")
async def chat(request: Request, q: str):
    config = {"configurable": {"thread_id": "1"}}

    async def event_generator():
        loop = asyncio.get_event_loop()
        stream = agent.stream(
            {"messages": [("user", q)]},
            config,
            stream_mode="messages",
        )

        for token, metadata in stream:
            if not isinstance(token, AIMessageChunk):
                continue
            reasoning = [b for b in token.content_blocks if b.get("type") in ("thinking", "reasoning")]
            text = [b for b in token.content_blocks if b.get("type") == "text"]

            if reasoning:
                payload = json.dumps({"type": "reasoning", "content": reasoning[0].get("reasoning", "")}, ensure_ascii=False)
                yield f"data: {payload}\n\n"
            if text:
                payload = json.dumps({"type": "text", "content": text[0].get("text", "")}, ensure_ascii=False)
                yield f"data: {payload}\n\n"

        yield f"data: {json.dumps({'type': 'end'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
