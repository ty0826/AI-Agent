from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

# 示例的的模版
example_template = PromptTemplate.from_template("单词:{word},反义词：{antonym}")

# 示例的数据
example_data = [
    {"word": '大', "antonym": "小"},
    {"word": "上", "antonym": "下"}
]
few_template = FewShotPromptTemplate(
    example_prompt=example_template,  # 示例数据的模版
    examples=example_data,  # 示例的数据
    prefix="请告诉我单词的反义词，我提供如下示例",  # 示例之前的提示词
    suffix="基于之前的示例告诉我，{input_word}的反义词是？",  # 示例之后的提示词
    input_variables=['input_word']
)
prompt_text = few_template.invoke(input={'input_word': "左"}).to_string()

model = Tongyi(model='qwen-max')
res = model.invoke(input=prompt_text)
print(res)
