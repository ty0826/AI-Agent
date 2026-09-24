void main(List<String> args) {
  Map transMap = {"name": "张三", "age": 20, "sex": "男"};
  print(transMap);
  String name = transMap["name"];
  print(name);
  transMap["age"] = 21; //可以直接赋值和取值
  print(transMap['age']);

  /**
   * forEach:循环集合
   * addAll:在尾部添加多个元素
   * containsKey:判断集合中是否包含指定的key
   * remove:删除指定的key
   * clear:清空集合
   */
  transMap.forEach((item, value) {
    print("$item:$value");
  });
  transMap.addAll({"address": "北京", "phone": "123456789"});
  print(transMap);
  transMap.containsKey('sex') ? print("包含sex") : print("不包含sex");

  transMap.remove('sex');

  transMap.containsKey('sex') ? print("包含sex") : print("不包含sex");

  transMap.clear();
  print(transMap);
}
