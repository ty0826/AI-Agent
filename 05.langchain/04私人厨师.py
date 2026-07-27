from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Dict, Any
from langchain.tools import tool


@tool(description='联网查询对应的食谱，以及做法')
def search_web(query: str) -> Dict[str, Any]:
    tavilySearchResults_data = TavilySearchResults(max_results=3)
    return tavilySearchResults_data.invoke(query)


agent = create_agent(
    model=ChatOpenAI(
        model='qwen3-max',
        api_key="sk-c083a4bb1e734f1f93395071fc32d818",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    ),
    tools=[search_web],
    checkpointer=InMemorySaver(),
    system_prompt='你是一个厨师，根据用户提问，先从自己的知识库获取相应的食谱知识，再调用工具联网搜索，再将两者整合在一起，一起返回给用户，告诉用户怎么去做，具体配料，具体时间'
)
config = {
    "configurable": {
        "thread_id": "1"
    }
}
agent.invoke({'messages': HumanMessage(
    content='你好，我是ty,我现在想学习做菜，现在你要做我的私人厨师助手，告诉我怎么做，比如应该备什么菜，什么料，具体步骤、用量')},
    config)

response = agent.stream({
    'messages': HumanMessage(content='宫保鸡丁应该怎么做？')
}, config, stream_mode='values')

for chunk in response:
    for message in chunk['messages']:
        print(message.content, end="", flush=True)
