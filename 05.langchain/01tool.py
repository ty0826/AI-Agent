from langchain.agents import create_agent
from langchain_openai.chat_models import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Dict, Any


@tool(description='网络搜索')
def serach_web(question: str) -> Dict[str, Any]:
    tavilySearchResults_data = TavilySearchResults(max_results=3)
    return tavilySearchResults_data.invoke(question)


agent = create_agent(
    model=ChatOpenAI(
        model='qwen3-max',
        api_key="sk-c083a4bb1e734f1f93395071fc32d818",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    ),
    tools=[serach_web],
    system_prompt='根据用户提问搜索最新消息'
)

question = HumanMessage(content='康熙500万中式台球冠军是谁')
response = agent.stream({
    "messages": [question],
}, stream_mode='values')
for chunk in response:
    for message in chunk['messages']:
        print(message.content)
