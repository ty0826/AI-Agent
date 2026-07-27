import operator
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Annotated, TypedDict
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from IPython.display import display, Image
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import os

model = ChatTongyi(model='qwen3.5-plus')

# os.environ["TAVILY_API_KEY"] = "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"


class State(TypedDict):
    question: str
    answer: str
    context: Annotated[list[str], operator.add]


def load_tavilySearch_results(state: State):
    try:
        tavilySearchResultsdata = TavilySearchResults(max_results=3)
        searchResults = tavilySearchResultsdata.invoke(state["question"])
        print(searchResults)
        format_message = "\n\n--\n\n".join(
            f'<Document href="{doc["url"]}">\n{doc.get("content", "")}\n</Document>'
            for doc in searchResults
        )
        return {"context": [format_message]}
    except Exception as e:
        return {"context": []}


def load_wink_result(state: State):
    try:
        search_docs = WikipediaLoader(
            query=state["question"],
            load_max_docs=2
        ).load()
        format_message_docs = "\n\n--\n\n".join(
            f'<Document source="{doc.metadata.get("source", "")}">\n{doc.page_content}\n</Document>'
            for doc in search_docs
        )
        return {"context": [format_message_docs]}
    except Exception as e:
        return {"context": []}


def get_answer(state: State):
    context = "\n\n".join(state["context"])
    question = state["question"]
    prompt = f"""根据以下上下文回答问题：{context}问题：{question}"""
    answer = ''
    for chunk in model.stream([
        SystemMessage(content=prompt),
        HumanMessage(content="请回答")
    ]):
        if chunk.content:
            answer += chunk.content
    return {"answer": answer}


builder = StateGraph(State)
builder.add_node('load_tavilySearch_results', load_tavilySearch_results)
builder.add_node('load_wink_result', load_wink_result)
builder.add_node('get_answer', get_answer)

builder.add_edge(START, 'load_tavilySearch_results')
builder.add_edge(START, 'load_wink_result')
builder.add_edge("load_tavilySearch_results", 'get_answer')
builder.add_edge("load_wink_result", 'get_answer')
builder.add_edge("get_answer", END)

os.makedirs('state_db', exist_ok=True)
memory = SqliteSaver(sqlite3.connect('state_db/12.db', check_same_thread=False))

graph = builder.compile(checkpointer=memory)
config = {
    "configurable": {
        "thread_id": '1'
    }
}
# res = graph.invoke({'question': '丁俊晖呢'}, config)
# print(res)
# for chunk in res:
#     if chunk.get('answer') is not None:
#         print(chunk.get('answer', ''), end='', flush=True)
