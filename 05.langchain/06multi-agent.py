from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from pprint import pprint
models = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


@tool(description='计算数据的平方根')
def square_root(x: float) -> float:
    return x ** 0.5


@tool(description='计算数据的平方')
def square(x: float) -> float:
    return x ** 2


subagent1 = create_agent(
    model=models,
    tools=[square_root]
)

subagent2 = create_agent(
    model=models,
    tools=[square]
)


##创建主代理
@tool(description='监管subagent1智能体')
def call_subagent_1(x: float) -> float:
    response = subagent1.invoke({"messages": [HumanMessage(content=f"计算一下{x}的平方根")]})
    return response['messages'][-1].content


@tool(description='监管subagent2智能体')
def call_subagent_2(x: float) -> float:
    response = subagent2.invoke({"messages": [HumanMessage(content=f'计算一下{x}的平方')]})
    return response['messages'][-1].content

main_agent = create_agent(
    model=models,
    tools=[call_subagent_1, call_subagent_2],
    system_prompt="你是一个智能助手，可以根据用户输入，自主判断调用哪个智能体，给用户最准确的回答"
)

response = main_agent.invoke({"messages": [HumanMessage(content='100的平方根是多少')]})
pprint(response)