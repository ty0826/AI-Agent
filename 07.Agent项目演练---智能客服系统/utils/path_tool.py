######路径的配置文件
import os
def get_project_root() -> str:
    """
    获取工程所在的根目录， return 字符串根目录
    """
    current_file = os.path.abspath(__file__)  # 当前文件的绝对路径
    current_dir = os.path.dirname(current_file)  # 当前文件的绝对目录
    project_root = os.path.dirname(current_dir)  # 获取到当前的根目录
    return project_root


def get_abs_path(path: str) -> str:
    """
    传递相对路径获取绝对路径
    """
    project_root = get_project_root()
    return os.path.join(project_root, path)
