from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage

agent = create_agent(
    model=ChatOpenAI(
        model='qwen3-max',
        api_key="sk-c083a4bb1e734f1f93395071fc32d818",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    ),
    checkpointer=InMemorySaver()
)

question = HumanMessage(content='你好，我是ty,今年26岁了')
config = {'configurable': {'thread_id': '1'}}
agent.invoke({
    'messages': [question]
}, config)
response = agent.invoke({
    'messages': [HumanMessage(content='我是谁')]
}, config)
print(response)
