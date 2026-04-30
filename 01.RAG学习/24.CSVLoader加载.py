from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path='./data/textCsv.csv',
    csv_args={
        "delimiter": '#',  # 自定义分隔符，默认‘，’
        "quotechar": '"',  # 指定带分隔符文本引号包围的是单引号还是双引号
        # "fieldnames": ['name', 'age', 'gender','hobby']  # 自定义表头，但是如果文本有表头了就不要说明
    },
    encoding='utf-8'
)

# document = loader.load()  # 一次性输出
# print(document, type(document))

for documents in loader.lazy_load():  # 一段一段输出
    print(documents)
