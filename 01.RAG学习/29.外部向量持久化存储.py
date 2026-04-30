from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma

# Chroma 持久化存储  InMemoryVectorStore 内存存储
store = Chroma(
    collection_name='test',  # 当前向量存储的名字，类似数据库名字
    embedding_function=DashScopeEmbeddings(),
    persist_directory='./chroma_db'  # 存储的文件夹
)

# loader = CSVLoader(
#     file_path='./data/info.csv',
#     encoding="utf-8",
#     source_column="source"
# )
# document = loader.load()
#
# store.add_documents(
#     documents=document,  # 被添加的文档，格式是List[Document,Document,......]
#     ids=['ids' + str(len) for len in range(1, len(document) + 1)]  # 给添加的文档提供ID
# )
# store.delete(['ids1', 'ids2'])

data = store.similarity_search('python很好学的', 4, filter={"source": '黑马程序员'})  # filter表示只获取source是黑马程序员的数据
print(data)
