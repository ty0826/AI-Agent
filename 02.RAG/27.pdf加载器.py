from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path='./data/陶宇-前端开发工程师.pdf',
    # encodings='utf-8',
    mode='single' #默认是page，每一页生成一个Document，single当做一个Document
)

document = loader.load()
# print(document)

for index, item in enumerate(loader.lazy_load()):
    print(index, item.page_content)
    print('*'*20)
