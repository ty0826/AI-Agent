import os, json
from typing import Sequence
from langchain_core.messages import message_to_dict, BaseMessage, _message_from_dict
from langchain_core.chat_history import BaseChatMessageHistory

def get_history(session_id):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return FileChatMessageHistory(session_id, os.path.join(base_dir, 'history_chart'))


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



