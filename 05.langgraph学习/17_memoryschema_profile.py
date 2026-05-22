""""
 @@@@@@@记忆结构化存储
"""
from langchain_openai import ChatOpenAI
from IPython.display import display, Image
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph, START, END, MessagesState
from pydantic import BaseModel, Field
from trustcall import create_extractor
from langchain_core.messages import SystemMessage, HumanMessage
import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"
model = ChatOpenAI(
    model='qwen-max',
    api_key="sk-1fababd8c9e74ee48c9f0487bf2323fe",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
memorySaver = InMemorySaver()
memoryStore = InMemoryStore()


class UserProfile(BaseModel):
    user_name: str = Field(description='用户姓名')
    user_location: str = Field(description='用户住址')
    interests: list[str] = Field(description='用户兴趣列表')


####是记忆文本结构化输出
trustcall_extractor = create_extractor(
    model,
    tools=[UserProfile],
    tool_choice='UserProfile',
)

MODEL_SYSTEM_MESSAGE = """你是一个乐于助人的助手，给用户提供个性化服务。
如果你对这个用户有历史记忆，要根据记忆提供回复。
这个是记忆内容（可能为空）:{memory}"""

TRUSTCALL_INSTRUCTION = """创建或者更新记忆（JSON文档），并且要纳入以下对话信息"""


def get_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']
    namespace = ('memory', user_id)
    existing_memory = store.get(namespace, 'user_memory')###获取单个记忆
    if existing_memory and existing_memory.value:
        existing_dict = existing_memory.value
        formatted_memory = (
            f"Name:{existing_dict.get('user_name', '')}\n"
            f"Location:{existing_dict.get('user_location', '')}\n"
            f"Interests:{existing_dict.get('interests', '')}\n"
        )
    else:
        formatted_memory = None
    system_msg = MODEL_SYSTEM_MESSAGE.format(memory=formatted_memory)
    response = model.invoke([SystemMessage(content=system_msg)] + state['messages'])
    return {'messages': [response]}


def write_memory(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']
    namespace = ('memory', user_id)
    existing_memory = store.get(namespace, 'user_memory')
    existing_profile = {'UserProfile': existing_memory.value} if existing_memory else None
    result = trustcall_extractor.invoke({
        'messages': [SystemMessage(content=TRUSTCALL_INSTRUCTION)] + state['messages'],
        'profile': existing_profile
    })
    update_profile = result['responses'][0].model_dump() #转成字典结构
    key = 'user_memory'
    store.put(namespace, key, update_profile)


builder = StateGraph(MessagesState)
builder.add_node('get_memory', get_memory)
builder.add_node('write_memory', write_memory)
builder.add_edge(START, 'get_memory')
builder.add_edge('get_memory', 'write_memory')
builder.add_edge('write_memory', END)
graph = builder.compile(checkpointer=memorySaver, store=memoryStore)
# display(Image(graph.get_graph().draw_mermaid_png()))

config = {'configurable': {
    'thread_id': '1',
    'user_id': '1',
}}
input_messages = [HumanMessage(content='你好，我是ty')]
for chunk in graph.stream({'messages': input_messages}, config, stream_mode='values'):
    pass
    # chunk['messages'][-1].pretty_print()

input_messages = [HumanMessage(content="我喜欢在旧金山周围骑自行车")]

# Run the graph
for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"):
    pass
    # chunk["messages"][-1].pretty_print()

input_messages = [HumanMessage(content="我也喜欢去面包店")]

# Run the graph
for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"):
    pass
    # chunk["messages"][-1].pretty_print()

existing_memory = memoryStore.get(('memory', '1'), 'user_memory').dict()
print(existing_memory)