
##########模型可选
from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel, ChatTongyi
from utils.config_handler import rag_config
from langchain_community.embeddings import DashScopeEmbeddings


class BaseModalFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


#聊天模型
class ChatModalFactory(BaseModalFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_config['chart_model_name'])

#嵌入模型
class RagModalFactory(BaseModalFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_config['embedding_model_name'])


chat_modal_factory = ChatModalFactory().generator()
rag_modal_factory = RagModalFactory().generator()
