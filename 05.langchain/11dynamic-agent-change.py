from pprint import pprint
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage,ToolMessage,AIMessage

models = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

standard_agent = init_chat_model(
    'qwen3-max',
    model_provider="openai",
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
large_agent = init_chat_model(
    'qwen-plus',
    model_provider="openai",
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


@wrap_model_call
def state_based_model(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    message_count = len(request.messages)
    # 根据文本长度去判断掉哪个模型
    if message_count > 5:
        model = large_agent
    else:
        model = standard_agent
    request = request.override(model=model)
    return handler(request)


agent = create_agent(
    model=models,
    middleware=[state_based_model],
    system_prompt="你正在扮演生活中乐于助人的办公室实习生"

)

result = agent.invoke({
    "messages": [
        HumanMessage(content='你今天给办公室植物浇水了嘛 ')
    ]
})

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
})
pprint(response)
