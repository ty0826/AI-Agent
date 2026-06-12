from pprint import pprint
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langgraph.types import Command

models = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


@tool(description='阅读邮件信息')
def read_email(runtime: ToolRuntime) -> str:
    return runtime.state["email"]


@tool(description='发送邮件')
def send_email(runtime: ToolRuntime) -> str:
    return f"send email"


class Email_state(AgentState):
    email: str


agent = create_agent(
    model=models,
    tools=[read_email, send_email],
    state_schema=Email_state,  #
    checkpointer=InMemorySaver(),
    middleware=[HumanInTheLoopMiddleware(
        interrupt_on={
            "read_email": False,
            "send_email": True,  # 是否需要人类介入流程
        },
        description_prefix='发送邮件调用需要获得批准'
    )]
)
config = {'configurable': {"thread_id": "1"}}
agent.invoke({
    "messages": [HumanMessage(content='请阅读邮件并且帮我回复')],
    "email": "你好，小明，明天开会我要迟到了，我们可以改期再约嘛？"
}, config)
# 批准
result = agent.invoke(
    Command(
        resume={
            "decisions": [{"type": "approve"}]
        }
    ),
    config
)
# 拒绝
# result = agent.invoke(
#     Command(
#         resume={
#             "decisions": [
#                 {
#                     "type": "reject",
#                     "messages": "请不要毁约"
#                 }
#             ]
#         }
#     ),
#     config
# )

# 编辑
# result = agent.invoke(
#     Command(
#         resume={
#             "decisions": [
#                 {
#                     "type": "edit",
#                     "edited_action": {
#                         "name": "send_email",
#                         "args": {"body": "111"}
#                     }
#                 }
#             ]
#         }
#     ),
#     config
# )
pprint(result)
