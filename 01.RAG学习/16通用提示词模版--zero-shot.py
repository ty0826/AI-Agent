from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender}，你帮我起个名字，简单回答"
)
# 调用.fomate方法直接注入
# 如果直接使用注入方式，也可以使用prompt_template字符串形式，只不过不能基于chain链形式
# prompt_text = prompt_template.format(lastname='张', gender='女')
# models = Tongyi(models='qwen3-vl-235b-a22b-thinking')
# res = models.invoke(input=prompt_text)
# print(res)


# 基于chain链形式去写
model = Tongyi(model='qwen3-vl-235b-a22b-thinking')
chain = prompt_template | model
res = chain.invoke(input={"lastname": "陶", "gender": "女"})
print(res)
