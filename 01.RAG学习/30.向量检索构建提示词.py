from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings

modal = ChatTongyi(modle="qwen3-max")
prompts = ChatPromptTemplate.from_messages(
    [
        ('system', "以我提供的已知参考资料，回答一下问题，参考资料：{contentText}"),
        ('human', "用户提问：{input}")
    ]
)

store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model='text-embedding-v4')
)
store.add_texts(['减肥就要少吃多练，', '跑步就是很好的运动方式哦，', "少吃多动，"])
result = store.similarity_search('怎么减肥呢', 2)

message = '['
for chunk in result:
    message = message + chunk.page_content
message += ']'

chain = prompts | modal | StrOutputParser()
result_data= chain.invoke({'input': "怎么减肥呢", "contentText": message})
print(result_data)
