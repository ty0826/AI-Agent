# 使用langchain库
from langchain_community.llms.tongyi import Tongyi

# qwen3-vl-235b-a22b-thinking是聊天模型，qwen3-vl-235b-a22b-thinking是聊天模型
model = Tongyi(model="qwen3-vl-235b-a22b-thinking")

# 调用invoke向模型提问
res = model.invoke(input="你是谁")

print(res)
