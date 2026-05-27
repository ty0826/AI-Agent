# LangGraph + LangChain 多智能体（Multi-Agent）+ MCP + Skill 完整 Demo

# 这个 Demo 的目标：
#
# * 使用 `LangGraph` 构建多智能体协作
# * 使用 `LangChain` 管理 LLM / Tool
# * 模拟 MCP（Model Context Protocol）工具接入
# * 实现 Skill（技能）机制
# * 包含：
#
#   * Supervisor 调度
#   * 多 Agent 协作
#   * Tool 调用
#   * Memory
#   * Router
#   * State 管理
#   * 条件流转
#   * Skill 注册
#   * MCP Client 模拟
#
# 注意：
#
# 这个项目重点是：
#
# > “技术栈完整 + 学习用途”
#
# 不是生产级复杂工程。
#
# ---
#
# # 一、项目结构
#
# 建议目录：
#
# ```text
# multi_agent_demo/
# │
# ├── app.py
# ├── requirements.txt
# ├── .env
# │
# ├── agents/
# │   ├── researcher.py
# │   ├── coder.py
# │   └── planner.py
# │
# ├── skills/
# │   ├── weather_skill.py
# │   ├── python_skill.py
# │   └── search_skill.py
# │
# ├── mcp/
# │   └── mcp_client.py
# │
# └── memory/
#     └── memory_store.py
# ```
#
# 但为了方便学习，下面会直接给你：
#
# # 单文件完整版本
#
# 你可以直接运行。
#
# ---
#
# # 二、安装依赖
#
# ## requirements.txt
#
# ```txt
# langgraph
# langchain
# langchain-openai
# langchain-community
# python-dotenv
# openai
# duckduckgo-search
# ```
#
# 安装：
#
# ```bash
# pip install -r requirements.txt
# ```
#
# ---
#
# # 三、配置 API KEY
#
# ## .env
#
# ```env
# OPENAI_API_KEY=你的key
# ```
#
# ---
#
# # 四、完整代码（app.py）
#
# ```python
import os
import json
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    BaseMessage,
    SystemMessage,
)
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_community.tools import DuckDuckGoSearchRun

# =========================================================
# 1. ENV
# =========================================================


# =========================================================
# 2. LLM
# =========================================================

llm = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# =========================================================
# 3. MCP 模拟
# =========================================================

class MCPClient:
    """
    模拟 MCP Client

    实际生产里：
    - MCP Server
    - MCP Tool Discovery
    - MCP Resources
    - MCP Prompt

    都会通过协议通信。
    """

    def call_tool(self, tool_name: str, params: dict):
        print(f"\n[MCP] 调用工具: {tool_name}")
        print(f"[MCP] 参数: {params}\n")

        if tool_name == "weather":
            city = params.get("city", "未知城市")
            return f"{city} 今天晴天 25°C"

        if tool_name == "database":
            sql = params.get("sql")
            return f"SQL执行结果: {sql}"

        return "未知 MCP Tool"


mcp_client = MCPClient()


# =========================================================
# 4. Skills（技能系统）
# =========================================================
class SkillRegistry:
    """
    技能注册中心
    """

    def __init__(self):
        self.skills = {}

    def register(self, name, func):
        self.skills[name] = func

    def get(self, name):
        return self.skills.get(name)


skill_registry = SkillRegistry()
# =========================================================
# 5. Skills 定义
# =========================================================
search_tool = DuckDuckGoSearchRun()


@tool
def web_search(query: str) -> str:
    """搜索互联网信息"""
    return search_tool.run(query)


@tool
def weather_skill(city: str) -> str:
    """查询天气"""

    result = mcp_client.call_tool(
        "weather",
        {
            "city": city
        }
    )

    return result


@tool
def python_skill(code: str) -> str:
    """
    执行简单 Python 代码
    """

    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return str(local_vars)

    except Exception as e:
        return str(e)


# 注册 skill
skill_registry.register("search", web_search)
skill_registry.register("weather", weather_skill)
skill_registry.register("python", python_skill)

TOOLS = [
    web_search,
    weather_skill,
    python_skill
]


# =========================================================
# 6. Memory
# =========================================================

class SimpleMemory:
    """
    模拟长期记忆
    """

    def __init__(self):
        self.store = {}

    def save(self, user_id, key, value):
        if user_id not in self.store:
            self.store[user_id] = {}

        self.store[user_id][key] = value

    def load(self, user_id):
        return self.store.get(user_id, {})


memory = SimpleMemory()


# =========================================================
# 7. Graph State
# =========================================================
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_agent: str
    user_id: str


# =========================================================
# 8. Agent Factory
# =========================================================

def create_agent(system_prompt: str):
    agent_llm = llm.bind_tools(TOOLS)
    def agent_node(state: AgentState):
        memory_data = memory.load(state["user_id"])
        messages = [SystemMessage(
            content=f""" {system_prompt} 当前用户记忆： {json.dumps(memory_data, ensure_ascii=False)} """)
                   ] + list(state["messages"])
        response = agent_llm.invoke(messages)
        return {
            "messages": [response]
        }
    return agent_node


# =========================================================
# 9. 多智能体
# =========================================================
researcher_agent = create_agent(
    """
    你是 Researcher Agent。
    职责：
    - 搜索信息
    - 收集资料
    - 分析问题
    如果需要联网：
    使用 web_search。
    """
)

coder_agent = create_agent(
    """
    你是 Coder Agent。

    职责：
    - 编写代码
    - 调试代码
    - 解释代码

    如果需要运行代码：
    使用 python_skill。
    """
)

planner_agent = create_agent(
    """
    你是 Planner Agent。

    职责：
    - 制定计划
    - 拆分任务
    - 决定调用哪个 Agent
    """
)

# =========================================================
# 10. Supervisor
# =========================================================

SUPERVISOR_PROMPT = """
你是一个多智能体系统的 Supervisor。
你的职责：
- 判断当前任务应该交给哪个 Agent
- 只返回以下内容之一：
researcher
coder
planner
finish
规则：
- 搜索问题 -> researcher
- 编码问题 -> coder
- 复杂规划 -> planner
- 已完成 -> finish
"""

supervisor_llm = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def supervisor_node(state: AgentState):
    messages = [
                   SystemMessage(content=SUPERVISOR_PROMPT)
               ] + list(state["messages"])

    result = supervisor_llm.invoke(messages)

    next_agent = result.content.strip().lower()

    print(f"\n[Supervisor] 下一个 Agent: {next_agent}\n")

    return {
        "next_agent": next_agent
    }


# =========================================================
# 11. Tool Node
# =========================================================


tool_node = ToolNode(TOOLS)


# =========================================================
# 12. Router
# =========================================================


def router(state: AgentState):
    last_message = state["messages"][-1]

    # 如果 Agent 调用了 Tool
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return "supervisor"


# =========================================================
# 13. 构建 Graph
# =========================================================

workflow = StateGraph(AgentState)

# ------------------
# 添加节点
# ------------------

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("coder", coder_agent)
workflow.add_node("planner", planner_agent)
workflow.add_node("tools", tool_node)

# ------------------
# 入口
# ------------------

workflow.set_entry_point("supervisor")


# =========================================================
# 14. Supervisor 条件路由
# =========================================================


def supervisor_router(state: AgentState):
    next_agent = state["next_agent"]

    if next_agent == "researcher":
        return "researcher"

    if next_agent == "coder":
        return "coder"

    if next_agent == "planner":
        return "planner"

    return END


workflow.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "researcher": "researcher",
        "coder": "coder",
        "planner": "planner",
        END: END
    }
)

# =========================================================
# 15. Agent -> Tools / Supervisor
# =========================================================

workflow.add_conditional_edges(
    "researcher",
    router,
    {
        "tools": "tools",
        "supervisor": "supervisor"
    }
)

workflow.add_conditional_edges(
    "coder",
    router,
    {
        "tools": "tools",
        "supervisor": "supervisor"
    }
)

workflow.add_conditional_edges(
    "planner",
    router,
    {
        "tools": "tools",
        "supervisor": "supervisor"
    }
)

# =========================================================
# 16. Tool 执行后返回 Supervisor
# =========================================================

workflow.add_edge("tools", "supervisor")

# =========================================================
# 17. 编译 Graph
# =========================================================

app = workflow.compile()

# =========================================================
# 18. 测试
# =========================================================

if __name__ == "__main__":

    user_id = "user_001"

    memory.save(
        user_id,
        "favorite_language",
        "Python"
    )

    while True:

        query = input("\n用户:帮我搜索一下 LangGraph 是什么 ")

        if query == "exit":
            break

        result = app.invoke(
            {
                "messages": [
                    HumanMessage(content=query)
                ],
                "next_agent": "",
                "user_id": user_id
            }
        )

        print("\n================ 最终结果 ================\n")

        for msg in result["messages"]:
            print(f"{msg.type}: {msg.content}")
# ```
#
# ---
#
# # 五、运行
#
# ```bash
# python app.py
# ```
#
# 示例：
#
# ```text
# 用户: 帮我搜索一下 LangGraph 是什么
# ```
#
# 或者：
#
# ```text
# 用户: 帮我写一个快速排序
# ```
#
# 或者：
#
# ```text
# 用户: 北京天气怎么样
# ```
#
# ---
#
# # 六、这个 Demo 涉及到的核心技术
#
# ## 1. LangGraph
#
# 这里使用了：
#
# * StateGraph
# * Conditional Edge
# * Router
# * Node
# * ToolNode
# * State
# * Multi Agent
#
# ---
#
# ## 2. LangChain
#
# 这里使用了：
#
# * ChatOpenAI
# * Tool
# * Message
# * Tool Calling
# * Agent 构建
#
# ---
#
# ## 3. MCP（模拟）
#
# 这里虽然不是官方 MCP SDK。
#
# 但是已经模拟了：
#
# * MCP Tool Discovery
# * MCP Tool Call
# * 外部能力调用
#
# 后续你可以替换成：
#
# * Claude MCP
# * OpenAI MCP
# * FastMCP
# * Smithery
# * Supergateway
#
# ---
#
# ## 4. Skill（技能系统）
#
# 这里实现了：
#
# ```python
# skill_registry.register()
# ```
#
# 本质就是：
#
# ```text
# 技能名称 -> Tool/Function
# ```
#
# 真实生产里：
#
# * 技能市场
# * 技能版本
# * 技能权限
# * 技能动态加载
#
# 都会更复杂。
#
# ---
#
# ## 5. Supervisor 模式
#
# 这是现在非常主流的 Multi-Agent 架构。
#
# 结构：
#
# ```text
#                 Supervisor
#                  /   |   \
#                 /    |    \
#         Researcher Coder Planner
# ```
#
# Supervisor：
#
# * 负责任务拆分
# * Agent 调度
# * Agent 协调
#
# ---
#
# # 七、真实项目下一步怎么升级
#
# 你后面可以继续增加：
#
# ## 1. RAG
#
# 接入：
#
# * Chroma
# * FAISS
# * Milvus
# * PGVector
#
# ---
#
# ## 2. 长期记忆
#
# 替换成：
#
# * Redis
# * MongoDB
# * Postgres
# * Neo4j
#
# ---
#
# ## 3. 真正 MCP
#
# 推荐：
#
# * FastMCP
# * MCP Python SDK
# * Smithery
#
# ---
#
# ## 4. 多 Tool Agent
#
# 增加：
#
# * Browser Use
# * Playwright
# * SQL Agent
# * Code Interpreter
# * File System
# * GitHub Tool
#
# ---
#
# ## 5. Human In The Loop
#
# LangGraph 很适合：
#
# * 审批流
# * 中断恢复
# * 人工确认
# * 可视化工作流
#
# ---
#
# # 八、推荐学习路线
#
# 推荐顺序：
#
# ```text
# LangChain
#   ↓
# Tool Calling
#   ↓
# Agent
#   ↓
# LangGraph
#   ↓
# Multi-Agent
#   ↓
# Memory
#   ↓
# RAG
#   ↓
# MCP
#   ↓
# Workflow + HITL
# ```
#
# ---
#
# # 九、你下一步最建议做的事情
#
# 你现在不要直接冲复杂 Agent 平台。
#
# 建议：
#
# ## 第一步
#
# 先把这个 Demo 跑通。
#
# ---
#
# ## 第二步
#
# 自己新增：
#
# * 一个 Agent
# * 一个 Tool
# * 一个 Skill
#
# 比如：
#
# ```text
# Excel Agent
# PDF Agent
# SQL Agent
# ```
#
# ---
#
# ## 第三步
#
# 再做：
#
# ```text
# RAG + Multi-Agent
# ```
#
# ---
#
# ## 第四步
#
# 最后再接：
#
# ```text
# 真正 MCP
# ```
#
# 因为 MCP 本质是：
#
# ```text
# Tool 协议标准化
# ```
#
# 核心还是：
#
# ```text
# Agent + Tool + Workflow
# ```
#
# ---
#
# # 十、你后面还可以继续扩展
#
# 如果你需要，我还能继续给你：
#
# * 企业级目录结构
# * LangGraph 工作流最佳实践
# * DeepSeek + LangGraph
# * Qwen + LangGraph
# * AutoGen vs CrewAI vs LangGraph
# * MCP Server 真正实现
# * FastMCP 实战
# * 多 Agent 记忆共享
# * Agent 状态机
# * Agent 任务队列
# * Browser Agent
# * Code Agent
# * SQL Agent
# * ReAct Agent
# * Plan And Execute
# * Reflection Agent
# * Supervisor 架构升级
# * Swarm 架构
# * GraphRAG
# * Agent 权限系统
# * Agent Sandbox
