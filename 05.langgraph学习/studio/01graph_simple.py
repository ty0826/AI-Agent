from typing import TypedDict, Literal
import random
from IPython.display import display, Image
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    graph_state: str


def node1(state):
    print('--node1---')
    return {'graph_state': state['graph_state'] + 'I am'}


def node2(state):
    print('--node2---')
    return {'graph_state': state['graph_state'] + 'happy！'}


def node3(state):
    print('--node3---')
    return {'graph_state': state['graph_state'] + 'sad！'}


def decide_mood(state) -> Literal['node2', 'node3']:
    user_input = state['graph_state']

    if random.random() < 0.5:
        return 'node2'
    return 'node3'


###build graph
builder = StateGraph(State)
builder.add_node('node1', node1)
builder.add_node('node2', node2)
builder.add_node('node3', node3)

# logic
builder.add_edge(START, 'node1')
builder.add_conditional_edges('node1', decide_mood)
builder.add_edge('node2', END)
builder.add_edge('node3', END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

res = graph.invoke({'graph_state': 'I am'})

# print(res)
