# 配置文件
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 始终跟原文件平级

md5_path = os.path.join(BASE_DIR, 'md5.text')

collection_name = 'rag-chroma-db'
model = 'text-embedding-v4'
chartModel = 'qwen3.5-plus'
persist_directory = os.path.join(BASE_DIR, 'chroma-rag-db')

chunk_size = 1000
chunk_overlap = 50
separators = ['\n\n', '\n', '?', '!', '？', '！', '.', '。', ' ', '']
max_spilt_leng = 1000
similarty = 2

session_config = {
    "configurable": {
        "session_id": "user_001"
    }
}
