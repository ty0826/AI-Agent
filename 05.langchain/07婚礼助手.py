from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import Dict, Any, Optional
from langchain_core.tools import tool, ToolRuntime
from langchain.agents import AgentState, create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.types import Command
from pprint import pprint
import asyncio, os

os.environ["LANGCHAIN_TRACING_V2"] = "false"

models = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
"""航班信息，音乐，"""


async def main():
    client = MultiServerMCPClient(
        {
            "kiwi": {
                "transport": "streamable_http",
                "url": "https://mcp.kiwi.com"
            },
            "bing": {
                "transport": "stdio",
                "command": "npx",
                "args": ["-y", "bing-cn-mcp"]
            }
        }
    )
    tools_all = await client.get_tools()
    travel_tools = next(t for t in tools_all if t.name == 'search-flight')
    query_playlist_tools = next(t for t in tools_all if t.name == 'bing_search')

    travel_agent = create_agent(
        model=models,
        tools=[travel_tools],
        system_prompt="""你是一个飞机航班智能体，根据用户输入的出发地和目的地,出发时间，
搜索价格、时长、起飞时间、到达时间最优的航班方案。尽可能详细,你可能需要执行多次搜索，并逐步筛选，以找到最佳方案。"""
    )

    playlist_agent = create_agent(
        model=models,
        tools=[query_playlist_tools],
        system_prompt="""你是一个搜索音乐的智能体，根据用户提供的婚礼风格通过搜索，给用户提供合适场景的音乐,最终给用户提供一个音乐列表，你可能需要执行多次搜索，并逐步筛选，以找到最佳方案。"""
    )

    venue_agent = create_agent(
        model=models,
        tools=[query_playlist_tools],
        system_prompt="""
        你是一名场地（Venue）专家。
    请根据用户指定的位置和容量要求搜索合适的场地。
    你不允许再向用户提出任何额外的追问，
    你必须基于以下标准直接找到最佳场地选项：
    - 价格（越低越好）
    - 容量（与需求匹配度越高越好，最好完全匹配）
    - 评价（越高越好）
    你可能需要执行多次搜索，并逐步筛选，以找到最佳方案。"""
    )

    # 创建空状态
    class WeddingState(AgentState):
        origin: Optional[str] = None  # 出发地
        destination: Optional[str] = None  # 目的地
        guest_count: Optional[str] = None  # # 参加人数
        genre: Optional[str] = None  # # 风格
        start_time: Optional[str] = None

    @tool(description='调用航班信息智能体')
    async def search_flights(runtime: ToolRuntime) -> str:
        origin = runtime.state['origin']
        destination = runtime.state['destination']
        start_time = runtime.state['start_time']
        respones = await  travel_agent.ainvoke(
            {'messages': [HumanMessage(content=f"搜索时间为{start_time}从{origin}到{destination}的航班信息")]})
        return respones['messages'][-1].content

    @tool(description='调用音乐搜索智能体')
    async def search_palylist(runtime: ToolRuntime) -> str:
        genre = runtime.state['genre']
        respones = await playlist_agent.ainvoke(
            {"messages": [HumanMessage(content=f"搜索跟{genre}风格高度匹配的音乐")]})
        return respones['messages'][-1].content

    @tool(description='调用场地搜索智能体')
    async def search_venue(runtime: ToolRuntime) -> str:
        count = runtime.state['guest_count']
        genre = runtime.state['genre']
        destination = runtime.state['destination']
        respones = await venue_agent.ainvoke(
            {"messages": [HumanMessage(content=f"根据风格{genre}，人数{count}，区域{destination}，搜索对应的场地")]})
        return respones['messages'][-1].content

    @tool(description='更新智能体的状态')
    def update_state(origin: str | None = None, destination: str | None = None, guest_count: str | None = None,
                     genre: str | None = None, start_time: str | None = None, runtime: ToolRuntime = None):
        return Command(
            update={
                "origin": origin,
                "destination": destination,
                "guest_count": guest_count,
                "genre": genre,
                "start_time": start_time,
                "messages": [ToolMessage(content='状态更新成功！', tool_call_id=runtime.tool_call_id)]
            }
        )

    main_agent = create_agent(
        model=models,
        tools=[search_flights, search_venue, search_palylist, update_state],
        state_schema=WeddingState,
        system_prompt="""你是一名婚礼协调员，将航班，场地，和音乐播放列表等任务委派给你的专家处理，首先找到更新状态所需的所有信息。完成后，，你就可以分派任务了
                      一旦受到他们的回复，需要先更新信息，然后就可以为我协调一场完美的婚礼了"""
    )

    response = await main_agent.ainvoke({"messages": [
        HumanMessage(
            content='我是来自上海，应该要在2026年10月1日当天坐飞机出发到合肥去举办婚礼，大概有1000个人，婚礼风格我要现代简约一点，帮我筹备一下')]})
    pprint(response)


asyncio.run(main())
