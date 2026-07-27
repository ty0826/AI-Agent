from langchain_community.chat_models.tongyi import ChatTongyi
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, MessagesState
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

model = ChatTongyi(model='qwen3.5-plus')


@tool(description='计算两个数的乘积')
def multiply(a: int, b: int) -> int:
    return a * b


@tool(description='计算两个数的相和')
def add(a: int, b: int) -> int:
    return a + b


@tool(description='计算两个的相差')
def subtract(a: int, b: int) -> int:
    return a - b


tools = [multiply, add, subtract]
model_with_tool = model.bind_tools(tools)


##声明节点
def nodes(state: MessagesState):
    return {
        'messages': [
            model_with_tool.invoke(
                [
                    {
                        'role': 'system',
                        'content': '你是一个算术高手，擅长算数'
                    }
                ] + state['messages'])
        ]
    }


builder = StateGraph(MessagesState)
builder.add_node('nodes', nodes)
builder.add_node('tools', ToolNode(tools))

builder.add_edge(START, 'nodes')
builder.add_conditional_edges('nodes', tools_condition)
builder.add_edge('tools', 'nodes')

###加入会话记忆
# graph = builder.compile(MemorySaver())
graph = builder.compile()
config = {'configurable': {'thread_id': '1'}}
display(Image(graph.get_graph().draw_mermaid_png()))


# res = graph.stream({
#     'messages': [
#         {
#             'role': 'human',
#             'content': '再乘以3呢'
#         }
#     ]
# }, config, stream_mode='values')
# for chunk in res:
#     last_message = chunk['messages'][-1]
#     if last_message.content:
#         print(last_message.content)
