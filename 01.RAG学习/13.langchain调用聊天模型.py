from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage

# 得到模型对象
model = ChatTongyi(
    model="qwen3-vl-235b-a22b-thinking"
)
message = [
    SystemMessage(content="你是一个情感专家"),
    HumanMessage(content="女生生气了，说很烦，你该怎么办")
    # AIMessage(content="")
]

res = model.stream(
    input=message
)

for chunk in res:
    print(chunk.content, end="", flush=True)
