from langchain.agents.middleware import before_agent
from langchain.agents import AgentState, create_agent
from langchain.messages import RemoveMessage, ToolMessage, HumanMessage, AIMessage
from langgraph.runtime import Runtime
from typing import Any
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from pprint import pprint
from langchain.agents.middleware import SummarizationMiddleware

models = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


##删除消息
@before_agent  # 在agent启动前操作
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    messages = state['messages']
    tool_messages = [m for m in messages if isinstance(m, ToolMessage)]  # 找出工具信息，然后删除
    return {
        "messages": [RemoveMessage(id=m.id) for m in tool_messages],
    }


agent = create_agent(
    model=models,
    checkpointer=InMemorySaver(),
    middleware=[trim_messages]
)
sum_agent = create_agent(
    model=models,
    checkpointer=InMemorySaver(),
    middleware=[SummarizationMiddleware(
        model=models,
        trigger=("tokens", 50),  # 超过多少词元就触发总结
        keep=("messages", 1),  # 保留最后几条（1）数据
    )]
)
response = agent.invoke({
    "messages": [
        HumanMessage(
            content="我的设备无法开机。我该怎么办？"
        ),

        ToolMessage(
            content="正在启动 lorp-x7 初始诊断检测...",
            tool_call_id="1"
        ),

        AIMessage(
            content="设备是否已插上电源并且处于开启状态？"
        ),

        HumanMessage(
            content="是的，已经插上电源并且打开了。"
        ),

        ToolMessage(
            content="温度=42°C，电压=2.9V ... greeble 检测完成。",
            tool_call_id="2"
        ),

        AIMessage(
            content="设备上是否显示任何灯光或指示器？"
        ),

        HumanMessage(
            content="是的，它有一个红色指示灯亮着。"
        )
    ]
}, {
    "configurable": {
        "thread_id": "1"
    }
})
response1 = sum_agent.invoke({
    "messages": [
        HumanMessage(content="月球的首都是什么？"),
        AIMessage(content="月球的首都是月都（Lunapolis）。"),
        HumanMessage(content="月都的天气怎么样？"),
        AIMessage(content="天空晴朗，最高温120℃，最低温-100℃。"),
        HumanMessage(content="有多少奶酪矿工居住在月都？"),
        AIMessage(content="有10万名奶酪矿工居住在月都。"),
        HumanMessage(content="你觉得奶酪矿工工会会罢工吗？"),
        AIMessage(content="会，因为他们对新总统感到不满。"),
        HumanMessage(content="如果你是月都的新总统，你会如何回应奶酪矿工工会？")
    ]
}, {
    "configurable": {
        "thread_id": "2"
    }
})
pprint(response1)
