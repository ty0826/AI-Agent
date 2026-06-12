from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Any, Dict
from requests import get

load_dotenv()

mcp = FastMCP('mcp_server')


@mcp.tool(description='网络搜索问题资料')
def search_web(query: str) -> Dict[str, Any]:
    tavilySearchResults_data = TavilySearchResults(max_results=3)
    return tavilySearchResults_data.invoke(query)


@mcp.resource("github.com://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def github_file():
    url = f"https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/main/README.md"
    try:
        resp = get(url)
        return resp.text
    except Exception as e:
        return f"error: {e}"


@mcp.prompt()
def prompt():
    return """
    你是一个有帮助的助手，负责回答用户关于 LangChain、LangGraph 和 LangSmith 的问题。
    你可以使用以下工具/资源来回答用户的问题：
    search_web：在网络上搜索信息
    github_file：访问 langchain-ai 仓库中的文件
    如果用户提出的问题与 LangChain、LangGraph 或 LangSmith 无关，你应该回答：
    “对不起，我只能回答与 LangChain、LangGraph 或 LangSmith 相关的问题。”
    你可以多次调用工具和资源来回答用户的问题。
    你也可以向用户提出澄清问题，以便更好地理解他们的问题
"""
if __name__ == "__main__": mcp.run(transport="stdio")