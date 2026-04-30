#####生成md5文件
import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, JSONLoader
from langchain_core.documents import Document

from utils.logger_handle import logger


###获取md5文件
def get_md5_hash(file_path: str) -> str:
    if not os.path.exists(file_path):
        logger.error(f"[md5计算] 文件{file_path}不存在")
        return

    if not os.path.isfile(file_path):
        logger.error(f"[md5计算] 路径{file_path}不是文件")
        return

    md5_obj = hashlib.md5()
    chunk_size = 1024 * 4
    try:
        with open(file_path, "rb") as f:  # 读取文件，输出二进制’rb‘
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            md5_hexdigest = md5_obj.hexdigest()
            return md5_hexdigest
    except Exception as e:
        logger.error(f"计算文件{file_path}失败：{str(e)}")
        return


##返回文件夹内的文件列表
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]) -> tuple:
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_types

    for chunk in os.listdir(path):  # 查询path目录下面的所以文件夹和文件
        if chunk.endswith(allowed_types):  # 判断当前文件、文件夹是否合法
            files.append(os.path.join(path, chunk))  # 拼路径放到里面

    return tuple(files)


##阅读pdf文件
def pdf_loader(path: str, password: str = '') -> list[Document]:
    if password:
        return PyPDFLoader(path, password).load()
    else:
        return PyPDFLoader(path).load()


##阅读TXT文件
def txt_loader(path: str) -> list[Document]:
    return TextLoader(path, encoding='utf-8').load()


def json_loader(path: str) -> list[Document]:
    return JSONLoader(file_path=path,
                      jq_schema='.',  # .表示根
                      text_content=False,  # 抽取的不是字符串
                      json_lines=True,  # 抽取是一个JSONLine文件，每一行都是一个独立的json,
                      ).load()


def csv_loader(path: str) -> list[Document]:
    return CSVLoader(file_path=path,
                     csv_args={
                        "delimiter": '#',  # 自定义分隔符，默认‘，’
                        "quotechar": '"',  # 指定带分隔符文本引号包围的是单引号还是双引号
                        # "fieldnames": ['name', 'age', 'gender','hobby']  # 自定义表头，但是如果文本有表头了就不要说明
                    }).load()
