import requests
from lxml import html

target_url = 'https://www.tiobe.com/tiobe-index/'

response = requests.get(target_url)
document = html.fromstring(response.text)

###解析表头
# text=document.xpath('//table[1]/thead/tr/th/text()') #第一个table
text_thead = document.xpath('//table[@id="top20"]/thead/tr/th/text()')  # id为top20的表格
print(text_thead)  # ['Jul 2026', 'Jul 2025', 'Change', 'Programming Language', 'Ratings', 'Change']

# 解析数据
text_tbody = document.xpath('//table[1]/tbody/tr[last()]/td/text()')  ##最后一项数据
text_tbody_1 = document.xpath('//table[1]/tbody/tr[last()-1]/td/text()')  ##倒数第二项数据
print(text_tbody)  # ['20', '23', 'Ruby', '0.73%', '-0.02%']
print(text_tbody_1)  # ['19', '12', 'Fortran', '0.74%', '-0.93%']


##解析表格里的数据
table_list=document.xpath('//table[@id="top20"]/tbody/tr')
for table in table_list:
    tb_list=table.xpath('./td/text()')
    print(tb_list)

