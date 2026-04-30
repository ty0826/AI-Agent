from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

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
input_text = '怎么减肥呢？'

# message = '['
# for chunk in result:
#     message = message + chunk.page_content
# message += ']'
#
# chain = prompts | modal | StrOutputParser()
# result_data= chain.invoke({'input': "怎么减肥呢", "contentText": message})


# langchain中向量存储对象，有一个方法 as_retriever ,可以返回一个Runnable接口的子类实例对象
retrieve = store.as_retriever(search_kwargs={"k": 2})


def for_mat(doc: list[Document]):
    if not doc:
        return ''
    for_mat_str = '['
    for chunk in doc:
        for_mat_str += chunk.page_content
    for_mat_str += ']'
    return for_mat_str


chain = ({"input": RunnablePassthrough(), "contentText": retrieve | for_mat}) | prompts | modal | StrOutputParser()

"""
retrieve: 
        输入：用户的提问，字符串
        输出：向量库的检索结果，是个[Ducoment,....]
prompts:
        输入：用户提问+向量库的检索结果 是个DICT
        输出：输出一个完整的提示词 InputValue
"""
res = chain.invoke(input_text) #在这里输入的input_text会依次传入RunnablePassthrough和retrieve中，组成一个新的{}DICT
print(res)
