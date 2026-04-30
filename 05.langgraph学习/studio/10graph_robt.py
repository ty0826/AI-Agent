from langchain_community.chat_models.tongyi import ChatTongyi
from langgraph.graph import MessagesState, END, StateGraph, START
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.checkpoint.memory import MemorySaver  ###内存存储
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3  ###外部存储
import os
from IPython.display import Image, display
from typing import Literal

model = ChatTongyi(model='qwen3-max')


###默认的state中字段messages字段传递
class State(MessagesState):
    summary: str


###调用模型
def call_model(state: State):
    summary = state.get('summary', '')
    if summary:
        ##如果总结词存在就放入systemMessage中
        system_message = f"上下文总结:{summary}"
        messages = [SystemMessage(content=system_message)] + state['messages']
    else:
        messages = state['messages']

    repsonse = model.invoke(messages)
    return {'messages': [repsonse]}


###总结模型，调整消息
def summary_model(state: State):
    summary = state.get('summary', '')
    if summary:
        summary_message = (
            f'最新的总结:{summary}\n\n'
            '需要把现有的摘要添加到最新的摘要中'
        )
    else:
        summary_message = ('为上面对话生成一个总结')

    messages = state['messages'] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)
    ###只保留最新的两条记录
    delete_messages = [RemoveMessage(id=m.id) for m in state['messages'][:-2]]
    return {'summary': response.content, 'messages': delete_messages}


###是否要进行总结
def should_summary(state: State) -> Literal['summary_model', END]:
    messages = state.get('messages', [])
    if len(messages) > 6:
        return 'summary_model'
    return END


###添加记忆
workflow = StateGraph(State)

workflow.add_node('call_model', call_model)
workflow.add_node('summary_model', summary_model)

workflow.add_edge(START, 'call_model')
workflow.add_conditional_edges('call_model', should_summary)
workflow.add_edge('summary_model', END)

# memory = MemorySaver() ##内存存储

###外部存储
os.makedirs('state_db', exist_ok=True)
memory = SqliteSaver(sqlite3.connect('state_db/example.db', check_same_thread=False))

graph = workflow.compile(checkpointer=memory)

config = {'configurable': {'thread_id': '1'}}

res = input_message = graph.invoke({'messages': [HumanMessage(content='他什么时候出道的，什么时候隐退的，我要代表作')]}, config)
print(res)
