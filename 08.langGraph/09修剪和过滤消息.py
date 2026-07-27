from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
from langchain_community.chat_models.tongyi import ChatTongyi
from langgraph.graph import MessagesState, StateGraph, START, END

messages = [AIMessage('hi', id='1'), HumanMessage('我是ty', id='2')]
messages.append(AIMessage('我是个百科全书，对海洋生物知识了解的很多', name='AI', id='3'))
messages.append(HumanMessage('我只是知道珊瑚，其他的还有什么我需要学习的嘛', name='Human', id='4'))

llmModel = ChatTongyi(model='qwen3.5-plus')


def chart_modal(state: MessagesState):
    return {"messages": llmModel.invoke(state['messages'])}


####删除多余消息，只给模型传递最新的两条
def filter_messages(state: MessagesState):
    return {"messages": [RemoveMessage(id=m.id) for m in state['messages'][:-2]]}


builder = StateGraph(MessagesState)
builder.add_node('chart_modal', chart_modal)
builder.add_node('filter_messages', filter_messages)

builder.add_edge(START, 'filter_messages')
builder.add_edge('filter_messages', 'chart_modal')
builder.add_edge('chart_modal', END)
graph = builder.compile()

res = graph.invoke({'messages': messages})
print(res)
