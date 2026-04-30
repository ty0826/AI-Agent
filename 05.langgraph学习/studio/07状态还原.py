from typing import Annotated, TypedDict

from langchain_core.messages import RemoveMessage

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState


class CustomMessageState(TypedDict):
    message: Annotated[list[AnyMessage], add_messages]
    added_key_1: str
    added_key_2: str


class ExtendedMessageState(MessagesState):
    added_key_1: str
    added_key_2: str


###消息追加
from langchain_core.messages import AIMessage, HumanMessage

inittail_message = [AIMessage(content='hello', name='ty'), HumanMessage(content='world', name='ty1')]
new_message = AIMessage(content='hello', name='ty2')
res = add_messages(inittail_message, new_message)
print(res,'###消息追加')

###消息覆盖

inittail_message = [AIMessage(content='hello', name='ty', id='1'), HumanMessage(content='world', name='ty1', id='2')]
new_message = AIMessage(content='hello world', name='ty233',id='1')
res1 = add_messages(inittail_message, new_message)
print(res1,'###消息覆盖')


###消息删除
message=[AIMessage('hi',name='ty',id='1')]
message.append(HumanMessage('hello2222',name='ty',id='2'))
message.append(AIMessage('world333',name='ty',id='3'))
message.append(HumanMessage('world444',name='ty',id='4'))

del_meaasge=[RemoveMessage(id=m.id) for m in message[:-1]]
print(del_meaasge,'###消息删除*****')
print(message,'###消息删除')