from dataclasses import dataclass
from langchain.agents import create_agent, AgentState
from langchain.messages import HumanMessage, ToolMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver
from pprint import pprint


@tool(description='获取用户喜欢的颜色')
def get_favourite_color(runtime: ToolRuntime):
    return runtime.context.favourite_color


@tool(description='获取用户最喜欢的颜色')
def get_least_favourite_color(runtime: ToolRuntime):
    return runtime.context.least_favourite_color


@dataclass
class ColorContext:
    favourite_color: str = 'yellow'
    least_favourite_color: str = 'red'


class CustomState(AgentState):
    favourite_color: str


@tool(description='更新最喜欢的颜色工具')
def update_favourite_color(favourite_color: str, runtime: ToolRuntime):
    return Command(
        update={
            "favourite_color": favourite_color,
            "messages": [ToolMessage("成功更新最喜欢的颜色数据", tool_call_id=runtime.tool_call_id)]
        }
    )


@tool(description='处理自定义字段')
def read_favourite_color(runtime: ToolRuntime):
    try:
        return runtime.state['favourite_color']
    except KeyError:
        return '在状态里没有查询到最喜欢颜色数据'


agent = create_agent(
    model=ChatOpenAI(
        model='qwen3-max',
        api_key="sk-c083a4bb1e734f1f93395071fc32d818",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    ),
    tools=[update_favourite_color, read_favourite_color],
    checkpointer=InMemorySaver(),
    # context_schema=ColorContext
    state_schema=CustomState
)
config = {
    "configurable": {
        "thread_id": "1"
    }
}
response = agent.invoke(
    {"messages": [HumanMessage(content='我最喜欢的颜色是绿色')]},
    config,

)
response = agent.invoke(
    {"messages": [HumanMessage(content='我最喜欢什么颜色')]},
    config,

)
pprint(response)
