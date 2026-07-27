from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
import asyncio, sys


async def main():
    # {
    #     "time": {
    #         "transport": "stdio",
    #         "command": "uvx",
    #         "args": [
    #             "mcp-server-time",
    #             "--local-timezone=America/New_York"
    #         ]
    #     }
    # }
    client = MultiServerMCPClient(
        {
            "local_server": {
                "transport": "stdio",
                "command": sys.executable,
                "args": ["mcp_server.py"]
            }
        }
    )
    tools = await client.get_tools()
    resources = await client.get_resources('local_server')
    prompt = await client.get_prompt('local_server', 'prompt')
    prompt = prompt[0].content
    agent = create_agent(
        model=ChatOpenAI(
            model='qwen3-max',
            api_key="sk-c083a4bb1e734f1f93395071fc32d818",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        ),
        tools=tools,
        system_prompt=prompt,
    )

    config = {"configurable": {
        "thread_id": "1"
    }}
    response = await agent.ainvoke({"messages": [HumanMessage(content='请告诉我langsmith的原理')]}, config)
    print(response)


asyncio.run(main())
