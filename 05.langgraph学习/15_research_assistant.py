from langchain_core.messages import SystemMessage, HumanMessage, get_buffer_string, AIMessage
from pydantic import BaseModel, Field
from typing import List, TypedDict, Annotated
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_community.chat_models.tongyi import ChatTongyi
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader
import os
import operator
from IPython.display import display, Image, Markdown
from langgraph.types import Send

os.environ["TAVILY_API_KEY"] = "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"
thread = {'configurable': {'thread_id': '1'}}
memory = InMemorySaver()
model = ChatTongyi(model='qwen3-vl-235b-a22b-thinking')

os.environ["LANGCHAIN_TRACING_V2"] = "false"


class Analyst(BaseModel):
    affiliation: str = Field(description='分析师的所属结构')
    name: str = Field(description='分析师姓名')
    role: str = Field(description='分析师角色')
    description: str = Field(description='分析师的具体描述')

    @property  ###将personal方法伪装成属性，这样外部调用的时候，直接a.personal就直接调用了
    def personal(self):
        return f"name:{self.name}, affiliation:{self.affiliation}, role:{self.role},description:{self.description}"


class Perspecttives(BaseModel):
    analysts: List[Analyst] = Field(description='综合分析这些分析师的角色和组织架构')


class GenerateAnalystState(TypedDict):
    topic: str
    max_analysts: int
    human_analys_feedback: str
    analysts: List[Analyst]


def create_analysts(state: GenerateAnalystState):
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analys_feedback = state.get('human_analys_feedback', '')
    structured_model = model.with_structured_output(Perspecttives)
    system_message = f'你的任务是创建一组 AI 分析师角色，请严格遵循以下步骤：\n1. 阅读研究主题：{topic}\n2. 查看用户的反馈（如果有）：{human_analys_feedback}\n3. 基于主题识别最有趣的研究方向。\n4. 选择前 {max_analysts} 个最重要方向。\n5. 为每个方向分配一个分析师角色。'
    analysts = structured_model.invoke([SystemMessage(content=system_message), HumanMessage(content='生成分析师列表')])
    return {'analysts': analysts.analysts}


def human_feedback(state: GenerateAnalystState):
    pass


class InterviewState(MessagesState):
    max_num_turns: int
    context: Annotated[list, operator.add]
    analyst: Analyst
    interview: str
    sections: list


class SearchQuery(BaseModel):
    search_query: str = Field(description='用于搜索的查询')


####搜索数据图
def generate_question(state: InterviewState):
    analyst = state['analyst']
    messages = state['messages']
    system_messages = f"""你是一名分析师，需要采访专家以深入理解主题。\n你的目标是获取：\n1. 有趣的洞察（非显而易见）\n2. 具体的案例和细节\n你的分析方向如下：\n{
    analyst.personal}请先介绍自己，然后提出问题。\n持续追问直到完全理解主题。\n当完成时，请说："thank you help！"\n全程保持你的角色身份。"""
    question = model.invoke([SystemMessage(content=system_messages)] + messages)

    return {'messages': [question]}


search_instructions = """你将看到一段分析师与专家的对话。你的任务是把最后一个问题转换成一个适用于搜索引擎的查询。请分析整个对话，并重点关注最后一个问题。"""


def search_web(state: InterviewState):
    try:
        tavily_search = TavilySearchResults(max_results=3)
        structured_model = model.with_structured_output(SearchQuery)
        search_query = structured_model.invoke([SystemMessage(
            content=search_instructions)] + state['messages'])

        search_docs = tavily_search.invoke({'query': search_query.search_query})

        format_search_docs = '\n\n--\n\n'.join([
            f'<Document href={doc["url"]}>{doc["content"]}</Document>'
            for doc in search_docs
        ])
        return {'context': [format_search_docs]}
    except Exception as e:
        return {'context': []}


def search_wikipedia(state: InterviewState):
    try:
        structured_model = model.with_structured_output(SearchQuery)
        search_query = structured_model.invoke([SystemMessage(content=search_instructions)] + state['messages'])

        search_docs = WikipediaLoader(query=search_query.search_query, load_max_docs=2).load()

        format_search_docs = '\n\n--\n\n'.join([
            f'<Document source={doc["source"]} page="{doc.metadata.get("page", "")}">{doc["page_content"]}</Document>'
            for doc in search_docs
        ])

        return {'context': [format_search_docs]}
    except Exception as e:
        return {"context": []}


def generate_answer(state: InterviewState):
    analyst = state['analyst']
    messages = state['messages']
    context = state['context']
    system_message = f'"你是一名正在接受采访的专家。你的任务：根据提供的上下文回答问题。分析师关注点：{analyst.personal}上下文：{context}要求：1. 只能使用上下文中的信息2. 不要引入外部知识3. 必须标注来源（如 [1]）4. 在末尾列出所有引用来源'
    answers = model.invoke([SystemMessage(content=system_message)] + messages)
    answers.name = 'expert'
    return {'messages': [answers]}


def save_interview(state: InterviewState):
    messages = state['messages']
    interview = get_buffer_string(messages)
    return {'interview': interview}


def route_messages(state: InterviewState, nane: str = 'expert'):
    messages = state['messages']
    max_num_turns = state.get('max_num_turns', 2)
    num_responeses = len([m for m in messages if isinstance(m, AIMessage) and m.name == nane])
    if num_responeses >= max_num_turns:
        return 'save_interview'

    last_question = messages[-2]

    if 'thank you help' in last_question.content:
        return 'save_interview'
    return 'ask_question'


section_writer_instructions = """你是一名技术写作专家。
请根据以下资料撰写报告章节：
要求：
1. 使用 Markdown
2. ## 为标题
3. ### 为小节
4. 包含：标题 / 总结 / 来源

重点：
- 标题要吸引人（基于：{focus}）
- 总结要有洞察性（约400字）
- 必须使用来源标注 [1][2]
"""


def write_interview(state: InterviewState):
    interview = state['interview']
    context = state['context']
    analyst = state['analyst']
    system_message = section_writer_instructions.format(focus=analyst.description)
    section = model.invoke(
        [SystemMessage(content=system_message)] + [HumanMessage(content=f'根据上次文回答问题：{context}')])

    return {'sections': [section.content]}


interView_builder = StateGraph(InterviewState)
interView_builder.add_node('ask_question', generate_question)
interView_builder.add_node('search_web', search_web)
interView_builder.add_node('search_wikipedia', search_wikipedia)
interView_builder.add_node('generate_answer', generate_answer)
interView_builder.add_node('save_interview', save_interview)
interView_builder.add_node('write_interview', write_interview)

interView_builder.add_edge(START, 'ask_question')
interView_builder.add_edge('ask_question', 'search_web')
interView_builder.add_edge('ask_question', 'search_wikipedia')
interView_builder.add_edge('search_web', 'generate_answer')
interView_builder.add_edge('search_wikipedia', 'generate_answer')

interView_builder.add_conditional_edges('generate_answer', route_messages, ['ask_question', 'save_interview'])
interView_builder.add_edge('save_interview', 'write_interview')
interView_builder.add_edge('write_interview', END)


# Map-duce图
class ResearchGraphState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: str
    analysts: List[Analyst]

    sections: Annotated[list, operator.add]
    introduction: str
    content: str
    conclusion: str
    report: str


def initiate_all_interviews(state: ResearchGraphState):
    human_analyst_feedback = state.get('human_analyst_feedback', 'approve')
    if human_analyst_feedback.lower() != 'approve':
        return "create_analysts"
    else:
        topic = state.get('topic', '')
        return [Send('conduct_interview',
                     {
                         'analyst': item,
                         'topic': topic,
                         'messages': [HumanMessage(content=f"你正在研究主题：{topic}")]
                     }
                     )
                for item in state['analysts']
                ]


report_writer_instructions = """你是一名技术写作者，正在围绕以下总体主题撰写报告：

{topic}

你拥有一个分析师团队。每位分析师都完成了两件事：

1. 他们与某个特定子主题的专家进行了访谈。
2. 他们将研究发现整理成了一份备忘录（memo）。

你的任务：

1. 你将收到来自分析师们的一组备忘录。
2. 仔细思考每份备忘录中的洞见。
3. 将这些内容整合成一份清晰、简洁的总体总结，把所有备忘录中的核心思想串联起来。
4. 将每份备忘录中的关键点总结为一个连贯统一的叙述。

报告格式要求：

1. 使用 Markdown 格式。
2. 不要添加前言（pre-amble）。
3. 不要使用小标题（sub-heading）。
4. 使用一个一级标题开始报告：## Insights
5. 不要在报告中提及任何分析师姓名。
6. 保留备忘录中的引用标注，引用会以方括号形式出现，例如 [1] 或 [2]。
7. 创建一个最终整合后的参考来源列表，并添加一个标题为 `## Sources` 的章节。
8. 按顺序列出来源，并且不要重复。

[1] 来源 1
[2] 来源 2

以下是分析师们提供的备忘录，请基于它们撰写报告：

{context}
"""


def write_report(state: ResearchGraphState):
    sections = state['sections']
    topic = state['topic']
    formatted_str_section = '\n\n'.join(f'{section}' for section in sections)
    system_message = report_writer_instructions.format(topic=topic, context=formatted_str_section)
    report = model.invoke(
        [SystemMessage(content=system_message)] + [HumanMessage(content='根据这些备忘录撰写一份报告。')])
    return {'content': report.content}


intro_conclusion_instructions = """你是一名技术写作者，正在完成一份关于 {topic} 的报告。

你将会收到报告中的所有章节内容。

你的任务是撰写一个简洁、有吸引力的引言（Introduction）或结论（Conclusion）部分。

用户会指示你是写引言还是结论。

无论是哪一种，都不要添加任何前置说明（pre-amble）。

目标长度约为 100 个单词，要求简洁地：
- 对于引言：概括并预览报告中的所有章节内容。
- 对于结论：总结并回顾报告中的所有章节内容。

使用 Markdown 格式。

如果是撰写引言：
1. 创建一个有吸引力的标题，并使用 `#` 一级标题格式。
2. 使用 `## Introduction` 作为章节标题。

如果是撰写结论：
1. 使用 `## Conclusion` 作为章节标题。

以下是需要参考并进行总结的报告章节内容：
{formatted_str_sections}
"""


def write_introduction(state: ResearchGraphState):
    sections = state['sections']
    topic = state['topic']
    formatted_str_sections = '\n\n'.join(f'{section}' for section in sections)
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
    intro = model.invoke([SystemMessage(content=instructions)] + [HumanMessage(content='写引言')])
    return {'introduction': intro.content}


def write_conclusion(state: ResearchGraphState):
    sections = state['sections']
    topic = state['topic']
    formatted_str_sections = '\n\n'.join(f'{section}' for section in sections)
    instruction = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)
    intro = model.invoke([SystemMessage(content=instruction)] + [HumanMessage(content='写结论')])
    return {'conclusion': intro.content}


def final_report(state: ResearchGraphState):
    content = state["content"]
    if content.startswith("## Insights"):
        content = content.replace("## Insights", "")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = ""
    else:
        sources = ""
    final_report = (
            state["introduction"]
            + "\n\n---\n\n"
            + content
            + "\n\n---\n\n"
            + state["conclusion"]
    )
    if sources:
        final_report += "\n\n## Sources\n" + sources
    return {"report": final_report}


builder_report = StateGraph(ResearchGraphState)

builder_report.add_node('create_analysts', create_analysts)
builder_report.add_node('human_feedback', human_feedback)
builder_report.add_node('conduct_interview', interView_builder.compile())
builder_report.add_node('write_report', write_report)
builder_report.add_node('write_introduction', write_introduction)
builder_report.add_node('write_conclusion', write_conclusion)
builder_report.add_node('final_report', final_report)

builder_report.add_edge(START, 'create_analysts')
builder_report.add_edge('create_analysts', 'human_feedback')

builder_report.add_conditional_edges(
    'human_feedback',
    initiate_all_interviews,
    ['create_analysts', 'conduct_interview']
)

builder_report.add_edge('conduct_interview', 'write_report')
builder_report.add_edge('conduct_interview', 'write_introduction')
builder_report.add_edge('conduct_interview', 'write_conclusion')

builder_report.add_edge(
    ['write_report', 'write_introduction', 'write_conclusion'],
    'final_report'
)

builder_report.add_edge("final_report", END)
graph = builder_report.compile(checkpointer=memory, interrupt_before=['human_feedback'])
res = graph.invoke({'topic': 'langgraph的优势是啥', 'max_analysts': 3}, interrupt_before=['human_feedback'],
                   config=thread)
graph.update_state(thread, {"human_analyst_feedback": '增加一个Agent工程方向分析师'})
res1 = graph.invoke(None, config=thread)
graph.update_state(thread, {"human_analyst_feedback": 'approve'})
res1 = graph.invoke(None, config=thread)
report = res1.get('report', '')
print(res1)
Markdown(report)

# display(Image(graph.get_graph().draw_mermaid_png()))
