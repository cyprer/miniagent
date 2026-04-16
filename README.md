# MiniAgent

一个基于 LangChain + LangGraph 的轻量级 AI 对话 Agent，使用 MiniMax-M2.7 模型，支持思考过程流式输出。

## 功能特性

- 🤖 基于 LangGraph 的 Agent 架构
- 🧠 支持思考过程（Thinking）流式输出
- 💬 简单的命令行对话界面
- 💾 内置内存检查点（In-Memory Checkpointer）

## 环境要求

- Python >= 3.11
- MiniMax API Key（或其他兼容 Anthropic API 的后端）

## 安装

### 1. 克隆项目

```bash
git clone https://github.com/cyprer/miniagent.git
```

### 2. 创建虚拟环境

```bash
# 使用 uv（推荐）
uv venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows

# 或使用标准 venv
python -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
uv sync
# 或
pip install -r requirements.txt
```

## 配置

### 环境变量

复制 `.env.example` 为 `.env`，并填入你的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic
```

#### 配置说明

| 变量 | 说明 | 必需 |
|------|------|------|
| `ANTHROPIC_API_KEY` | 你的 API Key | 是 |
| `ANTHROPIC_BASE_URL` | API 基础URL，默认为 MiniMax 的 Anthropic 兼容端点 | 否 |

## 运行

```bash
python mini_agent.py
```

### 使用方法

启动后直接输入问题，Agent 会流式返回思考过程和回答：

```
对话已启动（输入 exit/quit/q 退出）:

你: 你好
🧠 思考: [thinking] 正在思考...
💬 回答: 你好！有什么可以帮助你的吗？

你: 解释一下量子计算
🧠 思考: [thinking] 这是一个关于量子计算的问题...
💬 回答: 量子计算是一种利用量子力学原理进行信息处理的计算方式...
```

输入 `exit`、`quit`、`q` 或 `退出` 可结束对话。

## 项目结构

```
miniagent/
├── mini_agent.py      # 主程序入口
├── pyproject.toml     # 项目配置
├── uv.lock           # 依赖锁定文件
├── .env              # 环境变量（不提交）
├── .env.example      # 环境变量示例
└── .gitignore        # Git 忽略配置
```

## 依赖

- [langchain](https://python.langchain.com/) >= 3.0 - LangChain 核心框架
- [langchain-anthropic](https://python.langchain.com/) >= 0.3 - Anthropic 模型集成
- [langgraph](https://langchain-ai.github.io/langgraph/) >= 0.2 - Agent 图结构
- [python-dotenv](https://pypi.org/project/python-dotenv/) >= 1.0 - 环境变量管理

## License

MIT
