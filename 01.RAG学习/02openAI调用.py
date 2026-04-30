from openai import OpenAI

# 配置openAI
client = OpenAI(
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)
# 调用模型
response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {
            "role": "system",
            "content": "你是一个python编程专家，并且不说废话简单回答问题"
        },
        {
            "role": "user",
            "content": "小明有2条宠物狗"
        }
    ]
)
print(response.choices[0].message.content)
