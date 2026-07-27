from typing import TypedDict, List, NotRequired
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from typing import Annotated
import operator


class Log(TypedDict):
    id: str
    question: str
    answer: str
    grade: NotRequired[int]
    grader: NotRequired[str]
    feedback: NotRequired[str]


###定义故障总结子图信息
class FailureAnalysisState(TypedDict):
    cleaned_logs: List[Log]
    failed_logs: List[str]
    fa_summary: str
    processed_logs: List[str]


class FailureAnalysisOutput(TypedDict):
    fa_summary: str
    processed_logs: List[str]


def get_failures(state):
    cleaned_logs = state['cleaned_logs']
    failures = [log for log in cleaned_logs if 'grade' in log]
    return {'failed_logs': failures}


def generate_summary(state):
    failures = state['failed_logs']
    fa_summary = '对 Chroma 文档的检索质量较差'
    return {'fa_summary': fa_summary, 'processed_logs': [f"日志分析--{log['id']}" for log in failures]}


fa_builder = StateGraph(FailureAnalysisState, input_schema=FailureAnalysisState, output_schema=FailureAnalysisOutput)
fa_builder.add_node('get_failures', get_failures)
fa_builder.add_node('generate_summary', generate_summary)

fa_builder.add_edge(START, 'get_failures')
fa_builder.add_edge('get_failures', 'generate_summary')
fa_builder.add_edge('generate_summary', END)


####故障分析生成报告子图信息
class QuestionSummaryState(TypedDict):
    cleaned_logs: List[Log]
    qs_summary: str
    processed_logs: List[str]
    report: str


class QuestionSummaryOutput(TypedDict):
    report: str
    processed_logs: List[str]


def generate_summaryReport(state):
    cleaned_logs = state['cleaned_logs']
    summary = '当前问题主要存在大模型和向量数据的调用上'
    return {'qs_summary': summary, 'processed_logs': [f"总结日志--{log['id']}" for log in cleaned_logs]}


def send_to_slack(state):
    qs_summary = state['qs_summary']
    report = '最后总结'
    return {'report': report}


su_builder = StateGraph(QuestionSummaryState, input_schema=QuestionSummaryState, output_schema=QuestionSummaryOutput)
su_builder.add_node('generate_summaryReport', generate_summaryReport)
su_builder.add_node('send_to_slack', send_to_slack)

su_builder.add_edge(START, 'generate_summaryReport')
su_builder.add_edge('generate_summaryReport', 'send_to_slack')
su_builder.add_edge('send_to_slack', END)


class EntryGraphState(TypedDict):
    raw_logs: List[str]
    cleaned_logs:  List[Log]
    fa_summary: str
    processed_logs: Annotated[List[str], operator.add]
    report: str


def clean_log(state):
    raw_logs = state['raw_logs']
    cleaned_logs = raw_logs
    return {'cleaned_logs': cleaned_logs}


entry_builder = StateGraph(EntryGraphState)
entry_builder.add_node('clean_log', clean_log)
entry_builder.add_node('question_summary', su_builder.compile())
entry_builder.add_node('question_failure', fa_builder.compile())

entry_builder.add_edge(START, 'clean_log')
entry_builder.add_edge('clean_log', 'question_failure')
entry_builder.add_edge('clean_log', 'question_summary')
entry_builder.add_edge('question_failure', END)
entry_builder.add_edge('question_summary', END)

graph = entry_builder.compile()
question_answer = Log(
    id='1',
    question='我可以导入大模型嘛',
    answer='想要导入大模型，需要从langchain中导入'
)
question_answer_feedback = Log(
    id='2',
    question='我怎么使用向量数据库',
    answer='使用向量数据库，例如rag=create_retriveal_chain(retriever,quetion_answer_chain)',
    grade=0,
    grader='文档查询',
    feedback=''
)
raw_logs = [question_answer, question_answer_feedback]
# res=graph.invoke({'raw_logs': raw_logs})

display(Image(graph.get_graph().draw_mermaid_png()))
