from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, MessagesState, START, END
from IPython.display import Image, display
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

model = ChatTongyi(model='qwen3-vl-235b-a22b-thinking')


@tool(description='计算两个数字的乘积')
def multiply(a: int, b: int) -> int:
    return a * b


model_with_tool = model.bind_tools([multiply])


def tool_calling_model(state: MessagesState):
    return {
        'messages': [model_with_tool.invoke(state['messages'])],
    }


builder = StateGraph(MessagesState)
builder.add_node('tool_calling_model', tool_calling_model)
builder.add_node('tools', ToolNode([multiply]))

builder.add_edge(START, 'tool_calling_model')

###根据用户输入的内容判断是否调用工具，还是直接跳过结束
builder.add_conditional_edges(
    'tool_calling_model',
    tools_condition
)
builder.add_edge('tools', END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))

res = graph.invoke({'messages': '11和22'})
# print(res)
