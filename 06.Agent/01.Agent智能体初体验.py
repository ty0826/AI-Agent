from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description='查询天气')
def get_weater() -> str:
    return '下雨天'

###构建智能体
agent = create_agent(
    model=ChatTongyi(model='qwen3-vl-235b-a22b-thinking'),  # 构建模型
    tools=[get_weater],  # 选择工具
    system_prompt='你是一个聊天助手，请回答用户问题'
)

res = agent.invoke({
    'messages': [
        {
            'role': 'human',
            'content': '明天南京天气怎么样?'
        }
    ]
})

for mes in res['messages']:
    print(type(mes).__name__, mes.content)
