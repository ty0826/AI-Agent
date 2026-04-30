from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime

"""
1、Agent调用前
2、Agent调用后
3、model调用前
4、model调用后
5、model调用中
6、tool调用中
"""


@before_agent
def before_agent(state: AgentState, runtime: Runtime) -> None:
    print( f"[before_agent]agent启动，并附带{len(state['messages'])}条消息")


@after_agent
def after_agent(state: AgentState, runtime: Runtime) -> None:
    print( f"[after_agent]agent启动完成，并附带{len(state['messages'])}条消息")


@before_model
def before_model(state: AgentState, runtime: Runtime) -> None:
    print( f"[before_model]modle即将调用，并附带{len(state['messages'])}条消息")


@after_model
def after_model(state: AgentState, runtime: Runtime) -> None:
    print( f"[after_model]modle调用完成，并附带{len(state['messages'])}条消息")


@wrap_model_call
def wrap_model(request, handler) -> None:
    print('模型调用中')
    return handler(request)


@wrap_tool_call
def wrap_tool(request, handler) -> None:
    print(f"工具执行：{request.tool_call['name']}")
    print(f"工具执行参数：{request.tool_call['args']}")
    return handler(request)

@tool(description='查询天气，传入城市名字，返回天气情况')
def get_weater(city: str) -> str:
    return f"城市{city}:下雨天"


agent = create_agent(
    model=ChatTongyi(model='qwen3-max'),
    tools=[get_weater],
    middleware=[before_agent, after_agent, before_model, after_model, wrap_model, wrap_tool]
)

res = agent.invoke({
    'messages': [
        {
            'role': 'human',
            "content": '今天南京天气怎么样？'
        }
    ]
})

for mes in res['messages']:
    print(type(mes).__name__, mes.content)
