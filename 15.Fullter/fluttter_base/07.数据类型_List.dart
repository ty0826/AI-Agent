void main(List<String> args) {
  List students = ["张三", "李四", "王五"];
  print(students);
  /**
   * add:在尾部添加元素
   * addAll:在尾部添加多个元素
   * remove:删除满足内容的第一个元素
   * removeLast:删除最后一个元素
   * removeRange:删除指定范围的元素
   */
  students.add("赵六");
  print(students);
  students.addAll(["小明", "小红"]);
  print(students);
  students.remove("李四");
  print(students);
  students.removeLast();
  print(students);
  students.removeRange(0, 2); //左闭右开
  print(students);

  /**
   * forEach:循环集合
   * every:判断集合中是否所有元素满足条件
   * where:筛选集合中满足条件的元素
   * length:获取集合长度
   * last:获取集合最后一个元素
   * first:获取集合第一个元素
   * isEmpty:判断集合是否为空
   */
  students.forEach((item) {
    print(item);
  });

  bool isAll = students.every((item) {
    return item.length > 1;
  });
  print(isAll);

  List newStudents = students.where((item) {
    return item.length > 1;
  }).toList();
  print(newStudents);

  print(students.length);

  print(students.last);

  print(students.first);

  print(students.isEmpty);
}
