""""
 @@@@@@@记忆存储
"""
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from IPython.display import display, Image
import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"
model = ChatTongyi(model='qwen-max')
memory = InMemorySaver()
memoryStore = InMemoryStore()
MODEL_SYSTEM_MESSAGE = """你是一个带有记忆功能的助手，可以根据用户信息提供个性化回复。如果你拥有关于该用户的记忆，请利用这些记忆来个性化你的回答以下是用户的记忆信息{memory}"""
# 根据聊天记录和已有记忆创建新的用户记忆
CREATE_MEMORY_INSTRUCTION = """你正在收集关于用户的信息，以便于你个性化的回复。当前用户信息：{memory} 
说明：
1、仔细查看下面的聊天记录
2、识别关于用户的新信息，例如：
    ~个人信息（姓名、所在地）
    ~偏好（喜欢、不喜欢）
    ~兴趣爱好
    ~过往经历
    ~目标或未来计划
3、将新信息与已有记忆合并
4、以清晰的项目符号列表格式整理记忆
5、如果新信息与旧信息产生冲突，请直接使用新信息

请记住：
只包含用户直接陈述的事实信息
不要进行假设和推断

请基于下面的聊天记录更新用户信息"""


def call_model(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']  # 从配置里获取userID
    namespace = ('memory', user_id)
    key = 'user_memory'
    existing_memory = store.get(namespace, key)  # 从存储获取上下文记忆
    if existing_memory:
        existing_memory_content = existing_memory.value.get('memory')
    else:
        existing_memory_content = '没有获取到记忆'
    system_msg = MODEL_SYSTEM_MESSAGE.format(memory=existing_memory_content)
    response = model.invoke([SystemMessage(content=system_msg)] + state['messages'])
    return {'messages': [response]}


def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']
    namespace = ('memory', user_id)
    key = 'user_memory'
    existing_memory = store.get(namespace, key)
    if existing_memory:
        existing_memory_content = existing_memory.value.get('memory')
    else:
        existing_memory_content = '没有获取到记忆'
    system_msg = CREATE_MEMORY_INSTRUCTION.format(memory=existing_memory_content)
    response = model.invoke([SystemMessage(content=system_msg)] + state['messages'])
    store.put(namespace, key, {'memory': response.content})


builder = StateGraph(MessagesState)
builder.add_node('call_model', call_model)
builder.add_node('write_memory', write_memory)
builder.add_edge(START, 'call_model')
builder.add_edge('call_model', 'write_memory')
builder.add_edge('write_memory', END)
graph = builder.compile(checkpointer=memory, store=memoryStore)

config = {"configurable": {"thread_id": "1", "user_id": "1"}}

# User input
input_messages = [HumanMessage(content="你好，我是ty,你需要用中文回答我哦")]

# Run the graph
for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"):
    pass
    # chunk["messages"][-1].pretty_print()

# User input
input_messages = [HumanMessage(content="我喜欢环球旅行")]

# Run the graph
for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"):
    pass
    # chunk["messages"][-1].pretty_print()

user_id = "1"
namespace = ("memory", user_id)
existing_memory = memoryStore.get(namespace, "user_memory").dict()
print(existing_memory)
###打开一个新线程
config = {"configurable": {"thread_id": "2", "user_id": "1"}}

# input_messages = [HumanMessage(content="嗨！你推荐我去哪里骑自行车呢?")]
#
# for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"):
#     chunk["messages"][-1].pretty_print()
