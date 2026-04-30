# 使用langchain库
from langchain_community.llms.tongyi import Tongyi

# qwen3-max是聊天模型，qwen-max是聊天模型
model = Tongyi(model="qwen-max")

# 调用invoke向模型提问
res = model.invoke(input="你是谁")

print(res)
