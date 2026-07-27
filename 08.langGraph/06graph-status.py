from typing import TypedDict, Literal

from pydantic.v1 import validator, BaseModel

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
import random
from dataclasses import dataclass


def node2(state):
    return {'mood': 'happy'}


def node3(state):
    return {'mood': 'sad'}


def decide_mood(state) -> Literal['node2', 'node3']:
    if random.random() < 0.5:
        return 'node2'
    return 'node3'


"""
TypeDict实现

class TypeDictState(TypedDict):
    name: str
    mood: Literal["happy", "sad"]

 
buider = StateGraph(TypeDictState)
# res = graph.invoke({'name': 'happy'})
"""

"""
使用DataClass实现


@dataclass
class DataClass:
    name: str
    mood: Literal["happy", "sad"]

def node1(state):
    return {'name': state.name + 'is .....'}

buider = StateGraph(DataClass)

res1=graph.invoke(DataClass(name='ty',mood='happy1'))
print(res1)
"""
"""
使用pydmic,当状态不对时直接抛出异常
"""


class PydmicState(BaseModel):
    name: str
    mood: Literal["happy", "sad"]

    @validator('mood')
    def mood_validator(cls, v):
        if v not in ['happy', 'sad']:
            raise ValueError('mood must be happy or sad')
        return v


def node1(state):
    return {'name': state['name'] + 'is .....'}


buider = StateGraph(PydmicState)
buider.add_node(node1, 'node1')
buider.add_node(node2, 'node2')
buider.add_node(node3, 'node3')

buider.add_edge(START, 'node1')
buider.add_conditional_edges('node1', decide_mood)
buider.add_edge('node2', END)
buider.add_edge('node3', END)

graph = buider.compile()
res1=graph.invoke(PydmicState(name='ty',mood='happy'))
print(res1)