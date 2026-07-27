from langchain.agents import create_agent

from agent.tools.agent_tools import rag_summarize, get_weather, get_user_id, get_current_month, get_user_location, fetch_external_data,  fill_context_for_report
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
from model.factory import chat_modal_factory
from utils.prompt_loader import load_main_prompts

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_modal_factory,
            system_prompt=load_main_prompts(),
            tools=[rag_summarize, get_weather, get_user_id, get_current_month, fetch_external_data, get_user_location,
                   fill_context_for_report],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

    def execult_stream(self, query):
        query_dict = {
            'messages': [
                {
                    'role': 'human',
                    'content': query
                }
            ]
        }
        ###第三个参数是切换提示词是把重置成false
        for chunks in self.agent.stream(query_dict, stream_mode='values', context={'report': False}):
            message = chunks['messages'][-1]
            if message.content:
                yield message.content.strip() + '\n'

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execult_stream('查询我当月的使用记录'):
        print(chunk,end='',flush=True)