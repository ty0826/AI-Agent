from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser  # 转字符串
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatTongyi(model="qwen3-max")
# prompt = PromptTemplate.from_template("你需要根据对话历史回应用户问题，对话历史:{chat_historys};用户当前输入:{input},请给出回应")
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', "你需要根据对话历史回答用户问题，对话历史："),
        MessagesPlaceholder('chat_history'),
        ("human", "{input}")
    ]
)


# 用于测试。打印日志函数
def getHistory(str):
    print("*" * 20, str.to_string(), "*" * 20)
    return str


chain = prompt | getHistory | model | StrOutputParser()

chat_history_store = {}
def get_history(session_id):
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]


# 通过RunnableWithMessageHistory获取一个新的带有历史记录功能的chain
conversaton_chain = RunnableWithMessageHistory(
    chain,  # 被附加历史消息的Runnable，通常chain
    get_history,  # 获取历史会话的函数
    input_messages_key="input",  # 声明用户输入消息在模版中的占位符
    history_messages_key="chat_history"  # 声明历史消息在模版中的占位符
)

if __name__ == '__main__':
    # 固定格式，。添加langchain的配置，为当前程序配置自己的sessionId
    session_config = {"configurable": {"session_id": "user_001"}}
    conversaton_chain.invoke({"input": "小明有一只狗"}, session_config)
    conversaton_chain.invoke({"input": "小刚有一只猫"}, session_config)
    conversaton_chain.invoke({"input": "小宇还有10只老虎"}, session_config)
    conversaton_chain.invoke({"input": "告诉我，那一共有几只宠物呀"}, session_config)
