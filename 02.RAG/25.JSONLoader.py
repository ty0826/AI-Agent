from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path='./data/stu_json_lines.json',
    jq_schema='.name',#.表示根
    text_content=False, #抽取的不是字符串
    json_lines=True #抽取是一个JSONLine文件，每一行都是一个独立的json
)

document = loader.load()
for documents in loader.lazy_load():
    print(documents.page_content)
