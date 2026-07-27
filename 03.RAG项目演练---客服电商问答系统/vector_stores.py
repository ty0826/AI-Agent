from langchain_chroma import Chroma
import config_data  as config


####查询数据
class VertorStoreService(object):
    def __init__(self, model):
        self.embedding = model
        self.vertor_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )

    def get_retrievice(self):
        return self.vertor_store.as_retriever(search_kwargs={'k': config.similarty})
