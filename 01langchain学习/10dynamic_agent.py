from dataclasses import dataclass
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from pprint import pprint

models = ChatOpenAI(
    model='qwen3-max',
    api_key="sk-c083a4bb1e734f1f93395071fc32d818",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


@dataclass
class LanguageContext:
    user_language: str = "Chinese"


@dynamic_prompt
def user_language_prompt(request: ModelRequest):
    user_language = request.runtime.context.user_language
    base_prompt = '你是一个智能助手'
    print(user_language)
    if user_language != 'Chinese':
        return base_prompt
    else:
        return f"{base_prompt}用{user_language}回答"


agent = create_agent(
    model=models,
    context_schema=LanguageContext,
    middleware=[user_language_prompt]
)
result = agent.invoke({
    "messages": [
        HumanMessage(content='你好')
    ]
},
    context=LanguageContext(user_language='English')
)

pprint(result)
