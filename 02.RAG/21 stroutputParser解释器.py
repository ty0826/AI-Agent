from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

parser = StrOutputParser()
model = ChatTongyi(model='qwen3-vl-235b-a22b-thinking')
prompt = PromptTemplate.from_template("我姓：{lastname},刚生了一个{gender},请帮我起一个名字")

chain = prompt | model | parser | model
res: AIMessage = chain.stream({"lastname": "陶", "gender": "女儿"})
for msg in res:
    print(msg.content, end='', flush=True)
