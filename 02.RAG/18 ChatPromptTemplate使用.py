from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompe_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个情感专家，可以帮我分析并解决回复我的一些问题"),
        MessagesPlaceholder('history'),
        ("human", "在帮我分析一下")
    ]
)

history_data = [
    ("human", "女生说今天很热，过几分钟就上班了，命很苦"),
    ("ai", "是的呀，都是这样，没那么离谱"),
    ("human", "你会安慰人不，怎么这么说，我是想要你给我正反馈的回应")
]
prompt_text = chat_prompe_template.invoke({"history": history_data}).to_string()

model = ChatTongyi(
    model="qwen3-vl-235b-a22b-thinking"
)
res = model.stream(prompt_text)
for chunk in res:
    print(chunk.content, end="", flush=True)
