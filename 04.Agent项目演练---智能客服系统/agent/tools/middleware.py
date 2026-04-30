###中间件工具
from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command

from utils.logger_handle import logger
from utils.prompt_loader import load_report_prompts, load_main_prompts


@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,  # 请求封装
        handler: Callable[[ToolCallRequest], ToolMessage | Command],  # 执行函数
) -> ToolMessage | Command:  # 工具执行的监控
    logger.info(f"[tool monitor]工具调用：执行工具名称：{request.tool_call['name']}")
    logger.info(f"[tool monitor]工具调用：执行入参：{request.tool_call['args']})")

    try:
        logger.info(f"[tool monitor]工具调用：{request.tool_call['name']}),执行成功")
        if request.tool_call['name'] == 'fill_context_for_report':
            request.runtime.context['report'] = True
        return handler(request)
    except Exception as e:
        logger.error(f"[tool monitor]工具调用：执行错误{str(e)}")
        raise e


@before_model  # 在模型执行前输出日志
def log_before_model(
        state: AgentState,  # 整个agent智能体的状态记录
        runtime: Runtime
):  # 记录整个执行过程中的上下文信息
    logger.info(f"[log_before_model]模型即将调用：带有{len(state['messages'])}条信息")
    logger.debug(f"[log_before_model]{type(state['messages'][-1].name)} {state['messages'][-1].content.strip()}")

    return None


@dynamic_prompt  # 动态切换提示词,每一次生成提示词之前，会调用这个工具
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get('report', False)
    if is_report:
        return load_report_prompts()

    return load_main_prompts()
