from langchain_community.chat_models.tongyi import ChatTongyi
from IPython.display import display, Image
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

model = ChatTongyi(model='qwen3-max')


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


def model_tool_node(state: MessagesState):
    return {
        'messages':
            [
                model_with_tool.invoke([{
                    'role': 'system',
                    'content': '你是一个算术高手，擅长算数'
                }] + state['messages'])
            ]
    }


builder = StateGraph(MessagesState)

builder.add_node('model_tool_node', model_tool_node)
builder.add_node('tools', ToolNode(tools))

builder.add_edge(START, 'model_tool_node')

###判断是否需要调用工具
builder.add_conditional_edges('model_tool_node', tools_condition)
###ReAct模式,在回到模型，看是输出结果还是继续调用工具
builder.add_edge('tools', 'model_tool_node')

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))
#
# res = graph.stream({'messages': [
#     {
#         'role': 'human',
#         'content': '1+1*15-12343*23+565*551'
#     }
# ]}, stream_mode='values')
# for chunk in res:
#     last_message = chunk['messages'][-1]
#     if last_message.content:
#         print(last_message.content)
