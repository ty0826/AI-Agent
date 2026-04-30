from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class InputState(TypedDict):
    question: str


class OverviewState(TypedDict):
    question: str
    answer: str
    notes: str


class OutputState(TypedDict):
    answer: str


def think_node(state: InputState):
    return {"answer": "bye", "notes": '....this is name ty'}


def answer_node(state: OverviewState):
    return {"answer": "bye ty"}


builder = StateGraph(OverviewState, input_schema=InputState, output_schema=OutputState)
builder.add_node('node1', think_node)
builder.add_node('node2', answer_node)

builder.add_edge(START, 'node1')
builder.add_edge('node1', 'node2')
builder.add_edge('node2', END)
graph = builder.compile()

res = graph.invoke({'question': 'hi'})
print(res)
