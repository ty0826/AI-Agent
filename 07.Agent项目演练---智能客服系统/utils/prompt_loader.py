######提示词工具，读取提示词
from utils.logger_handle import logger
from utils.path_tool import get_abs_path
from utils.config_handler import prompt_config


def load_main_prompts():
    try:
        main_prompts_path = get_abs_path(prompt_config['mian_prompt_path'])  # 从配置文件里获取配置并生成路径
    except KeyError as e:
        logger.error(f"[load_main_prompts]在yaml文件中并没有配置mian_prompt_path，{str(e)}")
        raise e

    try:
        return open(main_prompts_path, 'r', encoding='utf-8').read()  # 打开对应文件并解析
    except Exception as e:
        logger.error(f"[load_main_prompts]解析系统提示词错误，{str(e)}")
        raise e


def load_rag_prompts():
    try:
        rag_prompts_path = get_abs_path(prompt_config['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml文件中并没有配置rag_summarize_prompt_path，{str(e)}")
        raise e
    try:
        return open(rag_prompts_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析rag提示词错误，{str(e)}")
        raise e


def load_report_prompts():
    try:
        report_prompts_path = get_abs_path(prompt_config['report_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml文件中并没有配置report_prompt_path，{str(e)}")
        raise e
    try:
        return open(report_prompts_path, 'r', encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_report_prompts]解析报告提示词错误，{str(e)}")
        raise e



