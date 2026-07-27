#####构建完之后查询##############
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory

import config_data as config
from file_history_store import get_history
from vector_stores import VertorStoreService


def format_data(doc: list[Document]):
    if not doc:
        return ''
    message = ''
    for chunk in doc:
        print(chunk)
        message += f"文档片段：{chunk.page_content}\n文档元数据:{chunk.metadata}\n\n"
    return message


def temp1(val: dict) -> str:
    return val['input']


def temp2(val):
    valNew = {}
    valNew['input'] = val['input']['input']
    valNew['history'] = val['input']['history']
    valNew['context'] = val['context']
    return valNew


class RagService(object):
    def __init__(self):
        self.vertor_service = VertorStoreService(DashScopeEmbeddings(model=config.model))
        self.prompt_templete = ChatPromptTemplate.from_messages([
            ('system', '以我参考的文档为主，简洁的回答用户问题，参考资料{context}'),
            ('system', "你需要根据对话历史回答用户问题，对话历史："),
            MessagesPlaceholder('history'),
            ('human', '请回答用户问题:{input}')
        ])
        self.model = ChatTongyi(model=config.chartModel)
        self.chain = self.get_chain()

    def get_chain(self):
        retrievice = self.vertor_service.get_retrievice()
        chain = (
                {'input': RunnablePassthrough(),
                 'context': RunnableLambda(temp1) | retrievice | format_data
                 } | RunnableLambda(temp2) | self.prompt_templete | self.model | StrOutputParser()
        )

        convertion_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key='input',
            history_messages_key='history'
        )
        return convertion_chain
