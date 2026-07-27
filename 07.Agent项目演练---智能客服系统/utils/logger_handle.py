####日志的配置文件
import os
import logging
from datetime import datetime
from utils.path_tool import get_abs_path

# 日志的格式配置
"""
asctime:时间
name:名称
levelname：日志等级 error,info,debug
message:内容
filename:文件名
lineno:文件行数
"""
DEFAULT_LOGGING_CONFIG = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s -%(filename)s-%(lineno)d- %(message)s'
)


def get_logger(
        name: str = 'agent',
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file=None,
) -> logging.Logger:
    logger = logging.getLogger(name)  # 获取日志文件
    logger.setLevel(logging.DEBUG)  # 设置日志级别

    # 避免重复添加
    if logger.handlers:
        return logger

    # 日志的保存目录（惰性创建：仅在首次真正需要 logger 时创建）
    default_logging_path = get_abs_path("logs")
    os.makedirs(default_logging_path, exist_ok=True)

    # 配置控制台handler
    console_handle = logging.StreamHandler()
    console_handle.setLevel(console_level)
    console_handle.setFormatter(DEFAULT_LOGGING_CONFIG)
    logger.addHandler(console_handle)

    # 配置文件handler
    if not log_file:
        log_file = os.path.join(default_logging_path, f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")

    file_handle = logging.FileHandler(log_file, encoding="utf-8")
    file_handle.setLevel(file_level)
    file_handle.setFormatter(DEFAULT_LOGGING_CONFIG)
    logger.addHandler(file_handle)

    return logger


class _LazyLogger:
    """
    惰性 logger：import 时不创建 handler/文件/目录，
    仅在第一次调用 logger.xxx 时才初始化真实 logger。
    """
    def __init__(self):
        self._logger: logging.Logger | None = None

    def _get(self) -> logging.Logger:
        if self._logger is None:
            self._logger = get_logger()
        return self._logger

    def __getattr__(self, item):
        return getattr(self._get(), item)


logger = _LazyLogger()

