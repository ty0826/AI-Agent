from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

store = InMemoryVectorStore(embedding=DashScopeEmbeddings())  # 定义内存存储变量 DashScopeEmbeddings文本转向量模型

loader = CSVLoader(
    file_path='./data/info.csv',
    encoding='utf-8',
    source_column='source'  # 相当于主键
)
document = loader.load()
store.add_documents(
    documents=document,  # 被添加的文档，格式是List[Document,Document,......]
    ids=['ids' + str(len) for len in range(1, len(document) + 1)]  # 给添加的文档提供ID
)

store.delete(['ids1', 'ids2']) #删除向量

result= store.similarity_search('python是不是很容易学呀', 4) #匹配向量并返回4组
for chunk in result:
   print(chunk.page_content)
