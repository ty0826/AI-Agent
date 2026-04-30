from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi(model='qwen3-max')

messages=[
    ('system',' 你是一个情感专家'),
    ('human','女朋友生气了，说很烦，该怎么办'),
    # ('ai')
]

for chunk in model.stream(input=messages):
    print(chunk.content,end="===",flush=True)