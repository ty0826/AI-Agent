import json

data = {
    'name': '李小龙',
    "age": 11,
    "性别": '男'
}
# ensure_ascii 确保中文能正常展示
# json.dumps 返回json字符串
print(json.dumps(data, ensure_ascii=False))

# json.loads 返回Python字典或者python列表
json_str = '{"name":"周杰伦","age":11,"gender":"男"}'
list_str = '[{"name":"周杰伦","age":11,"gender":"男"}]'
res_dict = json.loads(json_str)
res_list = json.loads(list_str)

print(res_dict, type(res_dict))
print(res_list, type(res_list))
