from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain.agents import AgentState, create_agent
from langchain.messages import ToolMessage, HumanMessage
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse, dynamic_prompt, \
    HumanInTheLoopMiddleware
from typing import Callable
from langchain_openai import ChatOpenAI
from pprint import pprint

models = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


@dataclass
class EmailData:
    username: str = '2446217554@qq.com'
    password: str = '123456ty'


class AnthenticatedState(AgentState):
    authenticated: bool


@tool(description='检查收件箱并且查看最近的邮件')
def check_email():
    return """
        你好，小明，我下周去上海，想问问我们能不能一起喝一杯咖啡？
        ---此敬，ty（2446217554@qq.com）
    """


@tool(description="接受邮箱地址、主题、邮件正文作为参数，并返回发送成功后的提示信息")
def send_email(to: str, subject: str, content: str):
    return f"已经向{to}，发送邮件，主题为{subject}，正文为{content}"


@tool(description="鉴定用的账号密码，看是否有权限去操作邮箱")
def anthenticate(email: str, password: str, runtime: ToolRuntime) -> Command:
    is_success = (runtime.context.username == email and runtime.context.password == password)
    return Command(
        update={
            "authenticated": is_success,
            "messages": [
                ToolMessage(
                    f"{'鉴权成功' if is_success else '鉴权失败'}！",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        }
    )


@wrap_model_call
def dynamic_tool_call(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    authenticated = request.state.get('authenticated')
    tools = [check_email, send_email] if authenticated else [anthenticate]
    return handler(request.override(tools=tools))


authenticated_prompt = '你是一个智能助手，如果用户有权限，就可以查看邮件箱和发送邮件'
unauthenticated_prompt = '你是一个智能助手，可以鉴权用户是否有权限'


@dynamic_prompt
def dynamic_prompt_systtem(request: ModelRequest) -> str:
    authenticated = request.state.get('authenticated')
    prompt = authenticated_prompt if authenticated else unauthenticated_prompt
    return prompt


agent = create_agent(
    model=models,
    tools=[anthenticate, check_email, send_email],
    checkpointer=InMemorySaver(),
    state_schema=AnthenticatedState,
    context_schema=EmailData,
    middleware=[
        dynamic_tool_call,
        dynamic_prompt_systtem,
        HumanInTheLoopMiddleware(
            interrupt_on={
                "anthenticate": False,
                "check_email": False,
                "send_email": True
            }
        )
    ]
)

config = {"configurable": {
    "thread_id": "1"
}}
agent.invoke(
    {
        "messages": [
            HumanMessage(content='用户名2446217554@qq.com,密码123456ty')
        ],
    },
    context=EmailData(),
    config=config,
)
agent.invoke(
    {
        "messages": [
            HumanMessage(content='回复邮件')
        ],
    },
    context=EmailData(),
    config=config,
)
response = agent.invoke(
    Command(
        resume={
            "decisions": [{"type": "approve"}]
        }
    ),
    config
)
pprint(response)
