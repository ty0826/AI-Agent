from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from pydantic import Field, BaseModel
from utils.response import success_response
from crud.chat import graph

router_chatAI = APIRouter(prefix="/chatAi", tags=["AI智能客服"])


class Configurable(BaseModel):
    thread_id: str
    user_id: str


class chatClass(BaseModel):
    query: str = Field(..., description='用户输入关键词')
    configurable: Configurable


@router_chatAI.post("/chat")
async def chat(data: chatClass):
    # MessagesState 需要的 key 是 messages（列表），之前传成了 message（字符串），
    # 导致用户提问根本没进入对话状态，所以返回里看不到用户的问题。
    result = await graph.invoke(
        {'messages': [HumanMessage(content=data.query)]},
        config={
            "configurable": data.configurable.model_dump()
        }
    )

    # result['messages'] 是本轮完整对话历史，最后一条是 AI 的回复
    messages = result['messages']
    answer = messages[-1].content if messages else ''

    return success_response(
        data={
            'query': data.query,
            'answer': answer,
            # 完整对话历史（含用户提问与 AI 回复），方便前端展示
            'history': [
                {'role': m.type, 'content': m.content}
                for m in messages
            ],
        },
        messages="AI智能返回成功！"
    )
