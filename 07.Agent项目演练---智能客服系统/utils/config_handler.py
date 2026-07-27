####配置文件
import yaml
from utils.path_tool import get_abs_path


####加载rag配置文件
def load_rag_config(config_path: str = get_abs_path('config/rag.yaml'), encoding: str = 'utf-8') -> dict:
    with open(config_path, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


###加载向量数据库配置文件
def load_chroma_config(config_path: str = get_abs_path('config/chroma.yaml'), encoding: str = 'utf-8') -> dict:
    with open(config_path, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


###加载提示词配置文件
def load_prompt_config(config_path: str = get_abs_path('config/prompt.yaml'), encoding: str = 'utf-8') -> dict:
    with open(config_path, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_agent_config(config_path: str = get_abs_path('config/agent.yaml'), encoding: str = 'utf-8') -> dict:
    with open(config_path, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


class _LazyConfig:
    """
    惰性配置：import 时不读 yaml，
    首次使用（如 cfg['key'] / cfg.get('key')）才加载并缓存。
    """

    def __init__(self, loader):
        self._loader = loader
        self._data: dict | None = None

    def _get_data(self) -> dict:
        if self._data is None:
            self._data = self._loader() or {}
        return self._data

    def __getitem__(self, key):
        return self._get_data()[key]

    def get(self, key, default=None):
        return self._get_data().get(key, default)

    def __contains__(self, key):
        return key in self._get_data()

    def keys(self):
        return self._get_data().keys()

    def items(self):
        return self._get_data().items()

    def values(self):
        return self._get_data().values()

    def __iter__(self):
        return iter(self._get_data())

    def __len__(self):
        return len(self._get_data())

    def __repr__(self):
        return repr(self._get_data())


rag_config = _LazyConfig(load_rag_config)
chroma_config = _LazyConfig(load_chroma_config)
prompt_config = _LazyConfig(load_prompt_config)
agent_config = _LazyConfig(load_agent_config)

if __name__ == '__main__':
    print(rag_config['chart_model_name'])
