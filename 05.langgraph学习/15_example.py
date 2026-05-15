import operator
from pydantic import BaseModel, Field
from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_community.document_loaders import WikipediaLoader
from langchain_tavily import TavilySearch  # updated 1.0
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, get_buffer_string
from langchain_openai import ChatOpenAI

from langgraph.constants import Send
from langgraph.graph import END, MessagesState, START, StateGraph

### LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)


### Schema

class Analyst(BaseModel):
    affiliation: str = Field(description="分析师所属机构")
    name: str = Field(description="分析师姓名")
    role: str = Field(description="分析师角色")
    description: str = Field(description="分析师关注点与动机描述")

    @property
    def persona(self) -> str:
        return f"姓名: {self.name}\n角色: {self.role}\n机构: {self.affiliation}\n描述: {self.description}\n"


class Perspectives(BaseModel):
    analysts: List[Analyst]


class GenerateAnalystsState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: str
    analysts: List[Analyst]


class InterviewState(MessagesState):
    max_num_turns: int
    context: Annotated[list, operator.add]
    analyst: Analyst
    interview: str
    sections: list


class SearchQuery(BaseModel):
    search_query: str = Field(description="用于搜索的查询")


class ResearchGraphState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: str
    analysts: List[Analyst]
    sections: Annotated[list, operator.add]
    introduction: str
    content: str
    conclusion: str
    final_report: str


### =========================
### Prompt（已中文化）
### =========================

analyst_instructions = """你的任务是创建一组 AI 分析师角色，请严格遵循以下步骤：
1. 阅读研究主题：
{topic}
2. 查看用户的反馈（如果有）：
{human_analyst_feedback}
3. 基于主题识别最有趣的研究方向。
4. 选择前 {max_analysts} 个最重要方向。
5. 为每个方向分配一个分析师角色。
"""


def create_analysts(state: GenerateAnalystsState):
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback', '')

    structured_llm = llm.with_structured_output(Perspectives)

    system_message = analyst_instructions.format(
        topic=topic,
        human_analyst_feedback=human_analyst_feedback,
        max_analysts=max_analysts
    )

    analysts = structured_llm.invoke(
        [SystemMessage(content=system_message)] +
        [HumanMessage(content="生成分析师列表")]
    )

    return {"analysts": analysts.analysts}


def human_feedback(state: GenerateAnalystsState):
    pass


question_instructions = """你是一名分析师，需要采访专家以深入理解主题。

你的目标是获取：
1. 有趣的洞察（非显而易见）
2. 具体的案例和细节

你的分析方向如下：
{goals}

请先介绍自己，然后提出问题。
持续追问直到完全理解主题。
当完成时，请说："非常感谢你的帮助！"

全程保持你的角色身份。
"""


def generate_question(state: InterviewState):
    analyst = state["analyst"]
    messages = state["messages"]

    system_message = question_instructions.format(goals=analyst.persona)

    question = llm.invoke(
        [SystemMessage(content=system_message)] + messages
    )

    return {"messages": [question]}


search_instructions = SystemMessage(content="""你将看到一段分析师与专家的对话。

你的任务是把最后一个问题转换成一个适用于搜索引擎的查询。

请分析整个对话，并重点关注最后一个问题。
""")


def search_web(state: InterviewState):
    tavily_search = TavilySearch(max_results=3)

    structured_llm = llm.with_structured_output(SearchQuery)

    search_query = structured_llm.invoke(
        [search_instructions] + state['messages']
    )

    data = tavily_search.invoke({"query": search_query.search_query})
    search_docs = data.get("results", data)

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}


def search_wikipedia(state: InterviewState):
    structured_llm = llm.with_structured_output(SearchQuery)

    search_query = structured_llm.invoke(
        [search_instructions] + state['messages']
    )

    search_docs = WikipediaLoader(
        query=search_query.search_query,
        load_max_docs=2
    ).load()

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}"/>\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}


answer_instructions = """你是一名正在接受采访的专家。

你的任务：根据提供的上下文回答问题。

分析师关注点：
{goals}

上下文：
{context}

要求：
1. 只能使用上下文中的信息
2. 不要引入外部知识
3. 必须标注来源（如 [1]）
4. 在末尾列出所有引用来源
"""


def generate_answer(state: InterviewState):
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    system_message = answer_instructions.format(
        goals=analyst.persona,
        context=context
    )

    answer = llm.invoke(
        [SystemMessage(content=system_message)] + messages
    )

    answer.name = "expert"

    return {"messages": [answer]}


def save_interview(state: InterviewState):
    messages = state["messages"]
    interview = get_buffer_string(messages)
    return {"interview": interview}


def route_messages(state: InterviewState, name: str = "expert"):
    messages = state["messages"]
    max_num_turns = state.get('max_num_turns', 2)

    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )

    if num_responses >= max_num_turns:
        return 'save_interview'

    last_question = messages[-2]

    if "非常感谢你的帮助" in last_question.content:
        return 'save_interview'

    return "ask_question"


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


def write_section(state: InterviewState):
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    system_message = section_writer_instructions.format(
        focus=analyst.description
    )

    section = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=f"资料如下：{context}")
    ])

    return {"sections": [section.content]}


interview_builder = StateGraph(InterviewState)

interview_builder.add_node("ask_question", generate_question)
interview_builder.add_node("search_web", search_web)
interview_builder.add_node("search_wikipedia", search_wikipedia)
interview_builder.add_node("answer_question", generate_answer)
interview_builder.add_node("save_interview", save_interview)
interview_builder.add_node("write_section", write_section)

interview_builder.add_edge(START, "ask_question")
interview_builder.add_edge("ask_question", "search_web")
interview_builder.add_edge("ask_question", "search_wikipedia")
interview_builder.add_edge("search_web", "answer_question")
interview_builder.add_edge("search_wikipedia", "answer_question")

interview_builder.add_conditional_edges(
    "answer_question",
    route_messages,
    ['ask_question', 'save_interview']
)

interview_builder.add_edge("save_interview", "write_section")
interview_builder.add_edge("write_section", END)


def initiate_all_interviews(state: ResearchGraphState):
    human_analyst_feedback = state.get('human_analyst_feedback', 'approve')

    if human_analyst_feedback.lower() != 'approve':
        return "create_analysts"

    topic = state["topic"]

    return [
        Send("conduct_interview", {
            "analyst": analyst,
            "messages": [HumanMessage(content=f"你正在研究主题：{topic}")]
        })
        for analyst in state["analysts"]
    ]


report_writer_instructions = """你是一名技术写作专家。

你的任务是整合所有分析师的报告。

要求：
1. 综合所有 memo
2. 提炼核心观点
3. 输出统一叙事结构
4. 不要出现分析师名字
5. 保留引用编号
6. 最后统一整理 Sources
"""


def write_report(state: ResearchGraphState):
    sections = state["sections"]
    topic = state["topic"]

    formatted = "\n\n".join(sections)

    report = llm.invoke([
        SystemMessage(
            content=report_writer_instructions.format(
                topic=topic
            )
        ),
        HumanMessage(content=formatted)
    ])

    return {"content": report.content}


intro_conclusion_instructions = """你是一名技术写作专家，正在完成关于 {topic} 的报告。

任务：
根据全部章节内容，生成：
- 引言 或
- 结论

要求：
1. 100字左右
2. Markdown格式
3. 引言必须有标题
4. 结论必须总结全文
"""


def write_introduction(state: ResearchGraphState):
    formatted = "\n\n".join(state["sections"])

    prompt = intro_conclusion_instructions.format(topic=state["topic"])

    intro = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="写引言")
    ])

    return {"introduction": intro.content}


def write_conclusion(state: ResearchGraphState):
    formatted = "\n\n".join(state["sections"])

    prompt = intro_conclusion_instructions.format(topic=state["topic"])

    conclusion = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="写结论")
    ])

    return {"conclusion": conclusion.content}


def finalize_report(state: ResearchGraphState):
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

    return {"final_report": final_report}


builder = StateGraph(ResearchGraphState)

builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)
builder.add_node("conduct_interview", interview_builder.compile())
builder.add_node("write_report", write_report)
builder.add_node("write_introduction", write_introduction)
builder.add_node("write_conclusion", write_conclusion)
builder.add_node("finalize_report", finalize_report)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")

builder.add_conditional_edges(
    "human_feedback",
    initiate_all_interviews,
    ["create_analysts", "conduct_interview"]
)

builder.add_edge("conduct_interview", "write_report")
builder.add_edge("conduct_interview", "write_introduction")
builder.add_edge("conduct_interview", "write_conclusion")

builder.add_edge(
    ["write_conclusion", "write_report", "write_introduction"],
    "finalize_report"
)

builder.add_edge("finalize_report", END)

graph = builder.compile(interrupt_before=['human_feedback'])