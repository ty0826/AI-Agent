from langchain_community.embeddings import DashScopeEmbeddings

# 创建模型对象，不传model默认使用text-embedding-v1模型
model = DashScopeEmbeddings()

# embed_query传入是单个字符串，embed_document传入的是list
print(model.embed_query('我喜欢你'))
print(model.embed_documents(['我喜欢你', "我爱你", "晚上吃啥"]))
