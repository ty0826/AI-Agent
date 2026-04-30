"""
总结服务类；用户提问，根据参考资料，将用户提问和参考资料整合提交给模型，让模型回复
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model.factory import chat_modal_factory
from rag.vector_store import VertorStoreService
from utils.prompt_loader import load_rag_prompts


def get_prompt(prompt_txt: str):
    return prompt_txt


class RagSummarizeReserve:
    def __init__(self):
        self.ver_store = VertorStoreService()
        self.document =self.ver_store.load_document()
        self.retrieve = self.ver_store.get_retriever()
        self.prompt_txt = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_txt)
        self.model = chat_modal_factory
        self.chain = self.get_chain()

    def get_chain(self):
        return self.prompt_template | get_prompt | self.model | StrOutputParser()

    def retrieve_doc(self, query: str) -> list[Document]:
        docs = self.retrieve.invoke(query)
        return docs

    def rag_summarize_doc(self, query: str) -> list[Document]:
        context_doc = self.retrieve_doc(query)

        context = ''
        count = 0
        for chunk in context_doc:
            count += 1
            context += f"【{count}:参考资料：{chunk.page_content}，参考原数据：{chunk.metadata}" + '\n'

        res = self.chain.invoke({
            'input': query,
            'context': context,
        })
        return res


if __name__ == '__main__':
    res = RagSummarizeReserve().rag_summarize_doc('小户型适合哪种扫地机器人')
    print(res)
