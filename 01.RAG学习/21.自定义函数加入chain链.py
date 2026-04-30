from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

str1 = PromptTemplate.from_template('我姓{lastname},生了个{gender},请告知我名字就行，任选一个')
str2 = PromptTemplate.from_template("姓名：{name},帮我解释这个名字含义")

strParser = StrOutputParser()
model = ChatTongyi(model='qwen3-max')

# my_function = RunnableLambda(lambda ai_messgae: {"name": ai_messgae.content})

chain = str1 | model | (lambda ai_messgae: {"name": ai_messgae.content}) | str2 | model | strParser
res: str = chain.stream(input={"lastname": '陶', "gender": "女儿"})
for chunk in res:
    print(chunk, end="", flush=True)
