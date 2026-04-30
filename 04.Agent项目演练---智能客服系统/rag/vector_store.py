#####实现向量存储库，。====检索向量增强
import os.path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from model.factory import rag_modal_factory
from utils.config_handler import chroma_config
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_md5_hash, json_loader, csv_loader
from utils.logger_handle import logger
from utils.path_tool import get_abs_path


class VertorStoreService:
    def __init__(self):
        ##初始化向量增强数据库
        self.vertor_store = Chroma(
            collection_name=chroma_config['collection_name'],
            embedding_function=rag_modal_factory,
            persist_directory=get_abs_path(chroma_config['persist_directory']),
        )
        # 初始化文件分割对象
        self.splitText = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config['chunk_size'],
            chunk_overlap=chroma_config['chunk_overlap'],
            separators=chroma_config['separators'],
            length_function=len
        )

    # 获取检索器对象
    def get_retriever(self):
        return self.vertor_store.as_retriever(search_kwargs={'k': chroma_config['k']})

    def load_document(self):
        """
        从数据文件夹里读取数据文件，转为向量数据库
        要计算文件的md5文件，去重
        """

        def check_md5_hex(md5_check: str):
            if not os.path.exists(get_abs_path(chroma_config['md5_hex_store'])):
                open(get_abs_path(chroma_config['md5_hex_store']), 'w', encoding='utf-8').close()  # 没有文件就先创建文件
                return False

            with open(get_abs_path(chroma_config['md5_hex_store']), 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line == md5_check:
                        return True
                return False

        def save_md5_hex(md5_check: str):
            with open(get_abs_path(chroma_config['md5_hex_store']), 'a', encoding='utf-8') as f:
                f.write(md5_check+'\n')

        def get_file_document(read_path: str):
            if read_path.endswith('txt'):
                return txt_loader(read_path)

            if read_path.endswith('pdf'):
                return pdf_loader(read_path)

            if read_path.endswith('json'):
                return  json_loader(read_path)

            if read_path.endswith('csv'):
                return csv_loader(read_path)

            return []

        ###读取文件夹下面的文件信息

        allowed_file_path: tuple[str] = listdir_with_allowed_type(
            get_abs_path((chroma_config['data_path'])),
            tuple(chroma_config['allow_knowledge_file_type'])
        )

        for path in allowed_file_path:
            md5_hex = get_md5_hash(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}已经存在知识库")
                continue

            try:
                documents: list[Document] = get_file_document(path)

                if not documents:
                    logger.warning(f'[加载知识库]{path}没有有效内容')
                    continue

                split_documents: list[Document] = self.splitText.split_documents(documents)

                if not split_documents:
                    logger.warning(f'[加载知识库]{path}分片没有有效内容')
                    continue

                ###存入向量数据库
                self.vertor_store.add_documents(split_documents)
                ###存入md5文件标识
                save_md5_hex(md5_hex)

                logger.info(f"[加载数据库]{path}内容加载完成")
            except Exception as e:
                ###exc_info为True时记录报错的详细信息，为false时仅记录报错本身
                logger.error(f"[加载数据库]{str(e)}加载失败", exc_info=True)
                continue


if __name__ == '__main__':
    vs = VertorStoreService()
    vs.load_document()
    retrieve = vs.get_retriever()
    res = retrieve.invoke('迷路')
    for doc in res:
        print(doc)
        print('*' * 20)
