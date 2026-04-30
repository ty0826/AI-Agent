from langchain_community.llms.tongyi import Tongyi

model = Tongyi(
    model="qwen-max",
)

# model的invoke是一次性返回，strem是流式输出
res = model.stream(input="你是谁")

for chunk in res:
    print(chunk, end="", flush=True)
