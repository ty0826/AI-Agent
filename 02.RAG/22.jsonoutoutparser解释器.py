from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate

srt1_template = PromptTemplate.from_template(
    "我姓：{lastname},刚生了一个{gender},请帮我起一个名字,简要回答，并转成json格式，严格返回key是name，值是其名字"
)

srt2_template = PromptTemplate.from_template("名字是{name},说明其含义")

json_template = JsonOutputParser()
str_template = StrOutputParser()
model = ChatTongyi(model="qwen3-vl-235b-a22b-thinking")

chain = srt1_template | model | json_template | srt2_template | model | str_template
res:AIMessage= chain.stream({"lastname":"殷","gender":'女儿'})
for item in res:
    print(item,end="",flush=True)
print(type(res))
