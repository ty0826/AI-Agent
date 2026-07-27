from openai import OpenAI

# 配置openAI
client = OpenAI(
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)
# 调用模型
response = client.chat.completions.create(
    model="qvq-max",
    messages=[
        {
            "role": "system",
            "content": "你是一个python编程专家，并且话非常多的简单回答问题"
        },
        {
            "role": "assistant",
            "content": "好的，我是一个编程专家,并且话非常多，你要问什么"
        },
        {
            "role": "user",
            "content": "输出一个九九乘法表"
        }
    ],
    stream=True
)

for chunk in response:
    print(
        chunk.choices[0].delta.content,
        end="",  # 每一段之间以空格分隔
        flush=True  # 立刻刷新缓冲区
    )

# print(response.choices[0].message.content)
# for i in range(1, 10):
#     for j in range(1, i + 1):
#         print(f"{j}×{i}={i*j}", end="\t")
#     print()
