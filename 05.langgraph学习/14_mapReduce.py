from langchain_community.chat_models.tongyi import ChatTongyi
import operator
from typing import Annotated, TypedDict

from pydantic import BaseModel
from langgraph.types import Send
from langgraph.graph import StateGraph, START, END
from IPython.display import display, Image

##主题模版

model = ChatTongyi(model='qwen3.5-plus')


class OverallState(TypedDict):
    topic: str
    subjects: list[str]
    jokes: Annotated[list[str], operator.add]
    best_selected_joke: str


class Subject(BaseModel):
    subjects: list[str]


####根据用户提示词返回主题列表
def generate_topic(state: OverallState):
    prompt = f"""根据用户主题，生成3到10个相关子主题。用户主题：{state['topic']}只返回Python列表格式。例如：["猫","狗","老虎"]"""
    response = model.invoke(prompt)
    return {'subjects': eval(response.content)}


###相当于遍历state['subjects']列表，调用generate_joke方法，入参subject，返回jokes
def contiune_to_joke(state: OverallState):
    return [Send("generate_joke", {'subject': s}) for s in state['subjects']]


class JokeState(TypedDict):
    subject: str


class Joke(BaseModel):
    joke: str

# 6068978321
###根据每个主题返回一个笑话
def generate_joke(state: JokeState):
    prompt = f'根据{state['subject']}都生成一个笑话'
    response = model.invoke(prompt)
    return {'jokes': [response.content]}


class BestJoke(BaseModel):
    id: int


def best_joke(state: OverallState):
    jokes = '\n\n'.join(
        [f"{i}. {j}" for i, j in enumerate(state['jokes'])]
    )
    prompt = f'主题：{state['topic']}下面是候选笑话：{jokes}请选择最好笑的一个。只返回对应的编号(id)，必须是整数。'
    response = model.invoke(prompt)
    idx = int(response.content.strip())
    return {
        'best_selected_joke': state['jokes'][idx]
    }


graph = StateGraph(OverallState)
graph.add_node('generate_topic', generate_topic)
graph.add_node('generate_joke', generate_joke)
graph.add_node('best_joke', best_joke)

graph.add_edge(START, 'generate_topic')
graph.add_conditional_edges('generate_topic', contiune_to_joke, 'generate_joke')
graph.add_edge('generate_joke', 'best_joke')
graph.add_edge('best_joke', END)
workFlow = graph.compile()
# res = workFlow.invoke({'topic': '动物'})
display(Image(workFlow.get_graph().draw_mermaid_png()))
