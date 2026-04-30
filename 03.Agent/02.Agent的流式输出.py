from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description='股价价格')
def get_price(name) -> str:
    return f"{name}的股价现在是20刀"


@tool(description='股市名称')
def get_info(name) -> str:
    return f"股票{name},是一个A股上市公司"


agent = create_agent(
    model=ChatTongyi(model='qwen3-max'),
    tools=[get_price, get_info],
    system_prompt='你是一个智能助手，可以回答股票相关问题，'
)

res = agent.stream(
    {
        'messages': [
            {
                'role': 'human',
                'content': '黑马股价多少，并介绍一下'
            }
        ]
    },
    stream_mode='values'
)

for chunk in res:
    last_message = chunk['messages'][-1]
    if last_message.content:
        print(type(last_message).__name__, last_message.content)
    try:
        if last_message.tool_calls:
            print(f"工具调用：{[tools['name'] for tools in last_message.tool_calls]}")
    except AttributeError as e:
        pass
