import os
import random

from langchain_core.tools import tool

from rag.rag_reserve import RagSummarizeReserve
from utils.config_handler import agent_config
from utils.logger_handle import logger
from utils.path_tool import get_abs_path

rag_store = RagSummarizeReserve()

usrId = ['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010']
months = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10',
          '2025-11', '2025-12']

extral_data = {}


@tool(description='从向量存储中检索参考资料')
def rag_summarize(query):
    return rag_store.rag_summarize_doc(query)


@tool(description='获取天气')
def get_weather(city) -> str:
    return f'{city}当前天气温度20度，晴天，适合出门'


@tool(description='获取定位')
def get_user_location() -> str:
    return random.choice(['南京', '合肥', '杭州'])


@tool(description='获取用户ID')
def get_user_id() -> str:
    return random.choice(usrId)


@tool(description='获取当前月份')
def get_current_month() -> str:
    return random.choice(months)


def get_data():
    external_data = get_abs_path(agent_config['user_month_history'])
    if not os.path.exists(external_data):
        raise FileNotFoundError(f'外部数据文件{external_data}不存在')

    with open(external_data, 'r', encoding='utf-8') as f:
        for chunk in f.readlines()[1:]:
            array: list[str] = chunk.strip().split(',')
            user_id: str = array[0].replace('"', '')
            feature: str = array[1].replace('"', '')
            cleaning_efficiency: str = array[2].replace('"', '')
            consumables: str = array[3].replace('"', '')
            compare: str = array[4].replace('"', '')
            time: str = array[5].replace('"', '')

            if user_id not in extral_data:
                extral_data[user_id] = {}

            extral_data[user_id][time] = {
                '特征': feature,
                '清洁效率': cleaning_efficiency,
                '耗材': consumables,
                '对比': compare,
            }


@tool(description='获取当前用户在指定时间的使用记录，如果检索到就已字符串形式返回，为检索到就空字符串')
def fetch_external_data(user_id: str, month: str) -> str:
    get_data()
    try:
        return extral_data[user_id][month]
    except KeyError:
        return logger.error(f"[fetch_external_data]未能检索到{user_id}在{month}的使用记录")


@tool(
    description='无入参，无返回值,调用后触发中间件自动为报告生成的场景动态注入上下午信息，为后续提示词切换提供上下午信息')
def fill_context_for_report():
    return 'fill_context_for_report工具已调用'


if __name__ == '__main__':
    res = fetch_external_data.invoke({'user_id': '1001', 'month': '2025-01'})
    print(res)
