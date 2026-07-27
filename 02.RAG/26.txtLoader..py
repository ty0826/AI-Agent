from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load = TextLoader(
    file_path='./data/python使用语法.txt',
    encoding='utf-8'
)

spilter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 分段的最大字数
    chunk_overlap=50,  # 分段之间允许重复的字数，为了文档的连贯性
    separators=["\n\n", "\n", "。", "!", "?", "！", "？", " ", ""],  # 需要分割的符号
    length_function=len  # 统计字符的依据，这里使用python的方法
)
doument = load.load()
splitDocument = spilter.split_documents(doument)
print(len(splitDocument))
for index, chunk in enumerate(splitDocument):  # enumerate 获取下标
    print(index, chunk.page_content)
