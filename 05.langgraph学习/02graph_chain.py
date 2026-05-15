from IPython.display import Image, display
from langchain_community.chat_models.tongyi import ChatTongyi
from langgraph.graph import MessagesState, START, END, StateGraph
from langchain_core.tools import tool

model = ChatTongyi(model='qwen3-vl-235b-a22b-thinking')


@tool(description='计算两个数的相乘积')
def multiply(a: int, b: int) -> int:
    return a * b


###给模型挂载工具
model_with_tool = model.bind_tools([multiply])


def tool_calling_model(state: MessagesState):
    return {'messages': [model_with_tool.invoke(state['messages'])]}


builder = StateGraph(MessagesState)
builder.add_node('tool_calling_model', tool_calling_model)

builder.add_edge(START, 'tool_calling_model')
builder.add_edge('tool_calling_model', END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))
"""
根据用户属于去识别是否调用工具
"""
# res = graph.invoke({'messages': '你好'})
res = graph.invoke({'messages': '4和20的积数多少'})
# print(res)
