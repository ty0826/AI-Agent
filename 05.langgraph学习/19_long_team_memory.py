""""
    构建长期记忆的智能体
"""
import os
import uuid
from datetime import datetime
from typing import Optional, Literal, TypedDict
from langchain_core.messages import SystemMessage, merge_message_runs, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from pydantic import BaseModel, Field
from trustcall import create_extractor

os.environ["LANGCHAIN_TRACING_V2"] = "false"

model = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


class Spy:
    def __init__(self):
        self.called_tools = []

    def __call__(self, run):
        q = [run]
        while q:
            r = q.pop()
            if r.child_runs:
                q.extend(r.child_runs)
            if r.run_type == 'chat_model':
                self.called_tools.append(r.outputs['generations'][0][0]['message']['kwargs']['tool_calls'])


###用户属性
class Profile(BaseModel):
    name: Optional[str] = Field(description='用户姓名', default=None)  # Optional--->name:str|None
    location: Optional[str] = Field(description='用户住址', default=None)
    job: Optional[str] = Field(description='用户职业', default=None)
    connections: list[str] = Field(description='用户的社会关系,例如家庭成员，朋友或者同事', default_factory=list)
    interests: list[str] = Field(description='用户的兴趣爱好列表', default_factory=list)


##代办属性
class ToDo(BaseModel):
    task: str = Field(description='待完成的任务')
    time_to_complete: str = Field(description='预计完成任务所需时间（分钟')
    deadline: Optional[datetime] = Field(description="任务需要完成的时间（如适用）", default=None)
    solutions: list[str] = Field(
        description='具体、可操作的解决方案列表（例如，与完成任务相关的具体想法、服务提供商或具体选项）',
        min_length=1,
        default_factory=list
    )
    status: Literal["not started", "in progress", "done", "archived"] = Field(
        description='任务状态',
        default="not started"
    )


MODEL_SYSTEM_MESSAGE = """你是一个乐于助人的聊天机器人。 
你被设计成用户的伴侣，帮助他们管理待办事项清单。
你的长期记忆会记录三件事：
1. 用户资料（关于用户的基本信息）
2. 用户的待办事项列表
3. 更新待办事项列表的一般说明
以下是当前的用户资料（如果尚未收集到任何信息，则可能为空）：
<user_profile>
{user_profile}
</user_profile>
以下是当前的待办事项列表（如果尚未添加任何任务，则可能为空）：
<todo>
{todo}
</todo>
以下是当前用户指定的待办事项列表更新偏好（如果尚未指定任何偏好，则可能为空）：
<instructions>
{instructions}
</instructions>
以下是关于用户消息推理的说明：
1. 仔细分析下面所呈现的用户信息。 
2. 决定是否需要更新你的长期记忆：
- 如果提供了用户的个人信息，请通过调用类型为“user”的UpdateMemory工具来更新用户的个人资料
- 如果提到了任务，请通过调用类型为“todo”的UpdateMemory工具来更新待办事项列表
- 如果用户已指定了关于如何更新待办事项列表的偏好，则通过调用类型为“instructions”的UpdateMemory工具来更新指令
3. 如有必要，告知用户您已更新内存：
- 不要告诉用户你已经更新了用户的个人资料
- 更新待办事项列表时，请通知用户
- 不要告诉用户你已经更新了说明
4. 宁可更新待办事项列表，也胜于什么都不做。无需征得明确许可。
5. 在用户调用工具以保存记忆后，或者如果没有调用工具，则自然地响应用户
"""
TRUSTCALL_INSTRUCTION = """反思以下互动。
使用提供的工具来保留关于用户的任何必要记忆。 
使用并行工具调用同时处理更新和插入操作。
系统时间：{time}"""

# 更新待办事项列表的说明
CREATE_INSTRUCTIONS = """反思以下互动。
根据此次互动，更新您关于如何更新待办事项列表项的说明。利用用户的任何反馈来更新他们希望添加项目的方式等。
您当前的指令是：
<current_instructions>
{current_instructions}
</current_instructions>"""


class UpdateMemory(TypedDict):
    update_type: Literal['user', 'todo', 'instructions']


def task_mAIstro(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']

    namespace = ('profile', user_id)
    memories = store.search(namespace)
    user_profile = memories[0].value if memories else None

    namespace = ('todo', user_id)
    memories = store.search(namespace)
    todo_memory = '\n'.join(f'{item.value}' for item in memories) if memories else ''

    namespace = ('instructions', user_id)
    memories = store.search(namespace)
    instructions_memory = memories[0].value if memories else None

    system_msg = MODEL_SYSTEM_MESSAGE.format(user_profile=user_profile, todo=todo_memory,
                                             instructions=instructions_memory)
    # parallel_tool_calls=False禁止模型并行调用多个工具
    response = model.bind_tools([UpdateMemory], parallel_tool_calls=False).invoke(
        [SystemMessage(content=system_msg)] + state['messages'])
    return {'messages': [response]}


def route_messages(state: MessagesState, config: RunnableConfig, store: BaseStore) -> Literal[
    END, 'update_todos', 'update_instructions', 'update_profile']:
    message = state['messages'][-1]  # 获取最新的一条数据
    if len(message.tool_calls) == 0:
        return END
    else:
        tool_call = message.tool_calls[0]
        if tool_call['args']['update_type'] == 'user':
            return 'update_profile'
        elif tool_call['args']['update_type'] == 'instructions':
            return 'update_instructions'
        elif tool_call['args']['update_type'] == 'todo':
            return 'update_todos'
        else:
            raise ValueError


profile_trustcall_create = create_extractor(
    model,
    tools=[Profile],
    tool_choice='Profile'
)


def update_profile(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']
    namespace = ('profile', user_id)
    existing_items = store.search(namespace)
    tool_name = 'Profile'
    existing_memory = ([(item.key, tool_name, item.value) for item in existing_items] if existing_items else [])
    TRUSTCALL_INSTRUCTION_FORMAT = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    update_messages = list(
        merge_message_runs(messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION_FORMAT)] + state['messages'][:-1]))
    result = profile_trustcall_create.invoke({'messages': update_messages, 'existing': existing_memory})
    for i, rmate in zip(result['responses'], result['response_metadata']):
        store.put(
            namespace,
            rmate.get('json_doc_id', str(uuid.uuid4())),
            i.model_dump(mode='json')
        )

    tool_calls = state['messages'][-1].tool_calls
    return {'messages': [{'role': 'tool', 'content': 'update profile', 'tool_call_id': tool_calls[0]['id']}]}


def extract_tool_info(tool_calls, schema_name='Memory'):
    changes = []
    for tool_call in tool_calls:
        for item in tool_call:
            if item['name'] == 'PatchDoc':
                changes.append({
                    'type': 'update',
                    'doc_id': item['args']['json_doc_id'],
                    'planned_edits': item['args']['planned_edits'],
                    'value': item['args']['patches'][0]['value']
                })
            elif item['name'] == schema_name:
                changes.append({
                    'type': 'new',
                    'value': item['args']
                })

    result_parts = []
    for change in changes:
        if change['type'] == 'update':
            result_parts.append(
                f"Document {change['doc_id']} updated:\n"
                f"Plan: {change['planned_edits']}\n"
                f"Added content: {change['value']}"
            )
        else:
            result_parts.append(
                f"New {schema_name} created:\n"
                f"Content: {change['value']}"
            )
    return '\n'.join(result_parts)


def update_todos(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']
    namespace = ('todo', user_id)
    existing_items = store.search(namespace)
    tool_name = 'ToDo'
    existing_memory = ([(item.key, tool_name, item.value) for item in existing_items] if existing_items else [])
    TRUSTCALL_INSTRUCTION_FORMAT = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    update_messages = list(
        merge_message_runs(messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION_FORMAT)] + state['messages'][:-1]))
    say = Spy()
    todo_extractor = create_extractor(
        model,
        tools=[ToDo],
        tool_choice='ToDo',
        enable_inserts=True,
    ).with_listeners(on_end=say)

    result = todo_extractor.invoke({'messages': update_messages, 'existing': existing_memory})
    for i, rmate in zip(result['responses'], result['response_metadata']):
        store.put(
            namespace,
            rmate.get('json_doc_id', str(uuid.uuid4())),
            i.model_dump(mode='json')
        )

    tool_calls = state['messages'][-1].tool_calls
    todo_update_msg = extract_tool_info(say.called_tools, tool_name)
    return {'messages': [{'role': 'tool', 'content': todo_update_msg, 'tool_call_id': tool_calls[0]['id']}]}


def update_instructions(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config['configurable']['user_id']
    namespace = ('instructions', user_id)
    key = 'user_instructions'
    existing_memory = store.get(namespace, key)
    system_msg = CREATE_INSTRUCTIONS.format(current_instructions=existing_memory.value if existing_memory else None)
    new_memory = model.invoke(
        [SystemMessage(content=system_msg)] + state['messages'][:-1] + [HumanMessage(content="请更新")])
    store.put(namespace, key, {'memory': new_memory})
    tool_calls = state['messages'][-1].tool_calls
    return {'messages': [{'role': 'tool', 'content': 'update instructions', 'tool_call_id': tool_calls[0]['id']}]}


builder = StateGraph(MessagesState)
builder.add_node('task_mAIstro', task_mAIstro)
builder.add_node('update_todos', update_todos)
builder.add_node('update_instructions', update_instructions)
builder.add_node('update_profile', update_profile)

builder.add_edge(START, 'task_mAIstro')
builder.add_conditional_edges('task_mAIstro', route_messages)
builder.add_edge('update_todos', 'task_mAIstro')
builder.add_edge('update_instructions', 'task_mAIstro')
builder.add_edge('update_profile', 'task_mAIstro')

memorySaver = InMemorySaver()
memoryStore = InMemoryStore()
graph = builder.compile(checkpointer=memorySaver, store=memoryStore)

config = {"configurable": {
    "thread_id": '1',
    "user_id": '1',
}}

input_messages = [HumanMessage(content='你好，我是ty,我生活在合肥')]
for chunk in graph.stream({'messages': input_messages}, config, stream_mode='values'):
    pass
    # chunk['messages'][-1].pretty_print()

input_messages = [HumanMessage(content='我明天要去一趟上海出差')]
for chunk in graph.stream({'messages': input_messages}, config, stream_mode='values'):
    pass
    # chunk['messages'][-1].pretty_print()
input_messages = [HumanMessage(content='不对，行程有变化我明天要去一趟北京出差,')]
for chunk in graph.stream({'messages': input_messages}, config, stream_mode='values'):
    pass

input_messages=[HumanMessage(content='在创建或更新待办事项时，请包含具体的本地商家/供应商')]
res= graph.invoke({'messages': input_messages}, config)
print(res)

# profile = memoryStore.search(('profile', '1'))
# todo = memoryStore.search(('todo', '1'))
# instructions = memoryStore.search(('instructions', '1'))
# print(profile)
# print('#' * 20)
# print(todo)
# print('#' * 20)
# print(instructions)
# print('#' * 20)
