###写入
# with open('./csv_data/01.csv', 'w', encoding='utf-8') as f:
#     f.write("姓名,性别,年龄,爱好\n")
#     f.write("小米,男,20,java\n")
#     f.write("小黄,女,23,python\n")
#     f.write("小红,女,25,'python,javascript'\n")

# 读
# with open('./csv_data/01.csv', 'r', encoding='utf-8') as f:
#     for line in f:
#         print(line.strip())

# 使用csv
import csv

# with open('./csv_data/01.csv', 'w', encoding='utf-8', newline='') as f:
#     writer = csv.DictWriter(f, fieldnames=["姓名", "性别", "年龄", "爱好"])
#     writer.writeheader()  # 写入表头
#     writer.writerow({"姓名": '小明', "性别": "男", "年龄": "12", "爱好": "java"})
#     writer.writerow({"姓名": '小红', "性别": "男", "年龄": "25", "爱好": "js"})
#     writer.writerow({"姓名": '小蓝', "性别": "男", "年龄": "46", "爱好": "javascript"})
#     writer.writerow({"姓名": '小黄', "性别": "女", "年龄": "26", "爱好": "java,python"})


with open('./csv_data/01.csv', 'r', encoding='utf-8' ) as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)