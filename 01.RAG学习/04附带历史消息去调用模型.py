from openai import OpenAI

# 配置openAI
client = OpenAI(
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)
# 调用模型
response = client.chat.completions.create(
    model="qwen3-vl-235b-a22b-thinking",  # 您可以按需更换为其它深度思考模型
    messages=[
        {
            "role": "system",
            "content": "你是一个AI助理，回答很简洁"
        },
        {
            "role": "user",
            "content": "小明有2条宠物狗"
        },
        {
            "role": "assistant",
            "content": "好的"
        },
        {
            "role": "user",
            "content": "小红有3只宠物狗"
        },
        {
            "role": "assistant",
            "content": "好的"
        },
        {
            "role": "user",
            "content": "总共有几只狗"
        },
    ],
    stream=True
)
for chunk in response:
    delta = chunk.choices[0].delta
    if delta.content != None:
        print(
            delta.content,
            end="=====",
            flush=True
        )
