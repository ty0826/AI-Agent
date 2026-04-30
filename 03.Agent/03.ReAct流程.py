from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool


@tool(description='这是我体重，输出单位是kg')
def get_weight():
    return 60


@tool(description='这是我的身高,输出单位是cm')
def get_cm():
    return 160


agent = create_agent(
    model=ChatTongyi(model='qwen3-max'),
    tools=[get_weight, get_cm],
    system_prompt='你是一个遵循ReAct流程的智能体，必须遵循【思考-行动-观察-在思考】流程解决问题 ，并且你要告诉我你的思考过程，工具的调用原因，按照【思考、行动、观察】结构告知我'
)

for chunk in agent.stream(
        {
            'messages': [
                {
                    'role': 'human',
                    'content': '请告诉我的BMI'
                }
            ]
        },
        stream_mode='values'
):
    last_message = chunk['messages'][-1]
    if last_message.content:
        print(type(last_message).__name__, last_message.content)
    try:
        if last_message.tool_calls:
            print(f"工具调用：{[tools['name'] for tools in last_message.tool_calls]}")
    except AttributeError as e:
        pass
