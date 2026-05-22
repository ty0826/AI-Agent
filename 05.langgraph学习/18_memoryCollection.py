""""
 @@@@@@@记忆集合
"""
import uuid
from langchain_core.messages import merge_message_runs
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.store.base import BaseStore
from pydantic import BaseModel, Field
from trustcall import create_extractor
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain.messages import SystemMessage, HumanMessage
import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"
model = ChatOpenAI(
    model='qwen3-vl-235b-a22b-thinking',
    api_key="sk-1fababd8c9e74ee48c9f0487bf2323fe",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


class Memory(BaseModel):
    content: str = Field(description='记忆的主要内容，例如：用户表示对学习法语感兴趣')


###创建一个结构化的信息提取器
trustcall_extractor = create_extractor(
    model,
    tools=[Memory],  ##告诉大模型，只能按照这个结果提取记忆
    tool_choice='Memory',  ##必须调用Memory这个tool
    enable_inserts=True,  # 新增记忆
    # enable_deletes=True, #删除记忆
    # enable_updates=True, #修改记忆
)

MODEL_SYSTEM_MESSAGE = """你是一个乐于助人的智能机器人，你被设计成用的贴心伴侣;
你拥有长期记忆，能够记录下你随时间了解到的用户信息;
当前记忆(可能包括本次对话中更新的记忆):{memory}"""

TRUSTCALL_INSTRUCTION = """反思以下互动，使用提供的工具来保留关于用户的任何必要的记忆，
并且使用并行工具调用同时处理更新和插入"""


###用历史记忆请求大模型获取信息
def call_model(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']
    namespace = ('memory', user_id)
    memoryview = store.search(namespace)  ###获取所有记忆信息
    content = '\n'.join(f'-{chunk.value["content"]}' for chunk in memoryview)
    system_message = MODEL_SYSTEM_MESSAGE.format(memory=content)
    response = model.invoke([SystemMessage(content=system_message)] + state['messages'])
    return {'messages': [response]}


###写入记忆
def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']
    namespace = ('memory', user_id)
    memoryview = store.search(namespace)  ###获取所有记忆信息
    tool_name = 'Memory'
    # memory 转成 LLM 输入格式
    existing_memory = ([(chunk.key, tool_name, chunk.value) for chunk in memoryview] if memoryview else None)
    ##merge_message_runs合并信息
    update_messages = list(
        merge_message_runs(messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION)] + state['messages']))
    ##调用大模型提取、更新Memory
    result = trustcall_extractor.invoke({'messages': update_messages, 'existing': existing_memory})
    # 'responses': [
    #     Memory(content='用户名叫ty。'),
    #     Memory(content='用户可能对与智能助手聊天感兴趣，因为这是他们开始互动时所做的。')],
    # 'response_metadata': [
    #     {'id': 'call_d37c3bdf5f49499dabc4b6'},
    #     {'id': 'call_b711580a6afa449e9d32db'}],
    # 'response_metadata': [{'id': 'call_7398c15413d84a6ea90ef3', 'json_doc_id': 'b23064e1-ae87-4a62-8767-05e0a330462b'},
    for r, rmeta in zip(result['responses'], result['response_metadata']):
        # --- 加上这两行代码 ---
        # 提前算好到底是用旧的，还是生成新的
        final_id = rmeta.get('json_doc_id', str(uuid.uuid4()))
        print(f"即将存入数据库的 记忆ID 是: {final_id}")
        store.put(
            namespace,
            final_id,
            r.model_dump(mode='json')
        )


builder = StateGraph(MessagesState)
builder.add_node('call_model', call_model)
builder.add_node('write_memory', write_memory)

builder.add_edge(START, 'call_model')
builder.add_edge('call_model', 'write_memory')
builder.add_edge('write_memory', END)

memorySaver = InMemorySaver()
memoryStore = InMemoryStore()
graph = builder.compile(checkpointer=memorySaver, store=memoryStore)

config = {'configurable': {
    'thread_id': '1',
    'user_id': '1'
}}

input_messages = [HumanMessage(content='你好，我是ty')]
for chunk in graph.stream({'messages': input_messages}, config, stream_mode='values'):
    pass

input_messages = [HumanMessage(content='我比较喜欢打篮球')]
for chunk in graph.stream({'messages': input_messages}, config, stream_mode='values'):
    pass

input_messages = [HumanMessage(content='其实我不喜欢大篮球了，喜欢打羽毛球')]
for chunk in graph.stream({'messages': input_messages}, config, stream_mode='values'):
    pass

# memory_view = memoryStore.search(('memory', '1'))
# # print(memory_view)
#
# for chunk in graph.stream({'messages': [HumanMessage(content='关于我你知道什么,并且给我一些建议')]},
#                           {'configurable': {'thread_id': '2', 'user_id': '1'}}, stream_mode='values'):
#     chunk['messages'][-1].pretty_print()
