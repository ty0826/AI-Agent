#####实现md5函数功能
import hashlib
import os
import config_data as config
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from datetime import datetime


def check_md5(md5_str: str):
    """
    检查传入的md5是否已经存入过，处理过得，未处理过得返回false ，处理返回ture
    """
    if not os.path.exists(config.md5_path):
        # 先查询有没有这个文件，没有文件的的话肯定就是没处理过了
        with open(config.md5_path, 'w', encoding='utf-8'):  # open打开文件，对应的地址没有文件就新建这个文件，然后打开在关闭
            return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():  # 读取对应路径文件的内容
            line = line.strip()  # 去空格和换行
            if line == md5_str:  # 比对内容，如果内容相同，肯定就处理过了，返回True
                return True
        return False


def save_md5(md5_str: str):
    # 打开文件，‘a’表示打开文件，并把内容追加到后面，并不会把之前的内容清空
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_md5(input_str: str, encodings='utf-8'):
    # 将传入的字符串转成md5格式
    str_bytes = input_str.encode(encoding=encodings)  # 将字符串转成bytes数组，为了下面md5对象更新内容
    # 创建md5对象
    md5_obj = hashlib.md5()  # 获取md5对象
    md5_obj.update(str_bytes)  # 更新内容，传入即将要转换的字节数组
    return md5_obj.hexdigest()  # 转成md5的16进制格式


# 存入数据库
class KnowledgeService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)  # 没有文件夹的时候就去创建文件夹，确保有
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model=config.model),
            persist_directory=config.persist_directory
        )  # 向量存储的实例Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )  # 文本分隔符的对象

    def upload_by_str(self, data: str, filename):
        # 将传入的字符串向量化，并存入数据库
        md5_str = get_md5(data)
        if check_md5(md5_str):
            return '【跳过】内容已经保存了'
        if len(data) > config.max_spilt_leng:
            knowLedgeChunk: list[str] = self.spliter.split_text(data)
        else:
            knowLedgeChunk = [data]

        chromaConfig = {
            'source': filename,
            'creattime': datetime.now().strftime('%Y-$M-%D %H:%M:%S'),
            'operator': 'TaoYU'
        }
        self.chroma.add_texts(
            knowLedgeChunk,
            metadatas=[chromaConfig for _ in knowLedgeChunk]
        )

        save_md5(md5_str)
        return '【成功】存入向量库'
