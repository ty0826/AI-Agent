import os, json
from typing import Sequence
from langchain_core.messages import message_to_dict, BaseMessage, _message_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory


# message_to_dict:单个消息对象（BaseMessage类实例）->字典
# _message_from_dict:[字典、字典]->[消息、消息]
# AIMessage，HumanMessage，SystemMessage都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id  # 会话ID
        self.storage_path = storage_path  # 不同的会话ID存储到不同的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)  # 完整的文件路径
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)  # 创建文件夹，确保文件夹存在

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages: list[BaseMessage] = list(self.messages) + list(messages)
        new_messages = [message_to_dict(m) for m in all_messages]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f, ensure_ascii=False)

    @property  # @property装饰器将message方法转成属性可以直接使用
    def messages(self) -> list[BaseMessage]:
        # 当前文件里内容是字符串，要先把转成字典->BaseMessagec才能去读取内容
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            if not raw:
                return []
            return [_message_from_dict(d) for d in raw]
        except FileNotFoundError:
            return []

    def clear(self) -> None:  # 清空内存存储
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False)


model = ChatTongyi(model="qwen3-vl-235b-a22b-thinking")
prompt = ChatPromptTemplate.from_messages([
    ('system', "你需要根据对话历史回答用户问题，对话历史："),
    MessagesPlaceholder('chat_history'),
    ("human", "{input}")
])


# 用于测试。打印日志函数
def getHistory(str):
    print("*" * 20, str.to_string(), "*" * 20)
    return str


chain = prompt | getHistory | model | StrOutputParser()


def get_history(session_id):
    return FileChatMessageHistory(session_id, './history_chart')


conversaton_chain = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",  # 声明用户输入消息在模版中的占位符
    history_messages_key="chat_history"  # 声明历史消息在模版中的占位符
)

if __name__ == '__main__':
    # 固定格式，。添加langchain的配置，为当前程序配置自己的sessionId
    session_config = {"configurable": {"session_id": "user_001"}}
    conversaton_chain.invoke({"input": "小明有一只狗"}, session_config)
    conversaton_chain.invoke({"input": "小刚有一只猫"}, session_config)
    conversaton_chain.invoke({"input": "小红还有10只老鼠"}, session_config)
    conversaton_chain.invoke({"input": "小宇还有10只老虎"}, session_config)
    conversaton_chain.invoke({"input": "告诉我，那一共有几只宠物呀"}, session_config)
