from langgraph.types import interrupt, Command
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict):
    value: list[str]


def ask_human(state: State):
    ###interrupt中断，执行到这边会停止
    answer = interrupt("What is your name?")
    return {"value": state['value'] + [f"name: {answer}!"]}


def ask_age(state: State):
    age = interrupt("How old are you?")
    return {"value": state['value'] + [f"age:{age}"]}


def final_step(state: State):
    return {"value": state['value'] + ["Done"]}


graph = (
    StateGraph(State)
    .add_node("ask_human", ask_human)
    .add_node("ask_age", ask_age)
    .add_node("final_step", final_step)
    .add_edge(START, "ask_human")
    .add_edge("ask_human", "ask_age")
    .add_edge("ask_age", "final_step")
    .add_edge("final_step", END)
    .compile(checkpointer=InMemorySaver())
)

config = {"configurable": {"thread_id": "1"}}

result = graph.invoke({"value": []}, config)  ###首次执行interrupt中断

while "__interrupt__" in result:
    # 获取 interrupt 提示词
    question = result["__interrupt__"][0].value

    # 用户输入
    user_input = input(f"{question} ")

    # resume
    result = graph.invoke(
        Command(resume=user_input),
        config
    )

print(result)

history = list(graph.get_state_history(config))  ###获取所有的历史状态
before_ask = [s for s in history if s.next == ("ask_human",)][-1]  ##找到 interrupt 前状态
print([s for s in history if s.next == ("ask_human",)][-1])

# replay_result = graph.invoke(None, before_ask.config)  ##time-travel，直接从checkponit之前执行也就是即将执行ask_human
fork_config = graph.update_state(before_ask.config, {"value": ["forked"]})  ###状态分叉，创建一个新的focked分支
fork_result = graph.invoke(None, fork_config)  ###interrupt再次中断

while "__interrupt__" in fork_result:
    # 获取 interrupt 提示词
    question = fork_result["__interrupt__"][0].value

    # 用户输入
    user_input = input(f"{question} ")

    # resume
    fork_result = graph.invoke(
        Command(resume=user_input),
        config
    )

print(fork_result)
# graph.invoke(Command(resume="Bob"), fork_config)  ####{"value": ["forked"，"Bob","DONE"]}
# res1 = graph.invoke(Command(resume="12"), config)
# print(res1)
