void main(List<String> args) {
  String name = "张三"; //声明字符串类型变量
  print(name);
  name = "李四"; //修改变量值
  print(name);
  //字符串拼接
  String content = '我的名字是${name}';
  print(content);
  String content2 = '我的名字是$name,今年12岁';
  print(content2);
}
