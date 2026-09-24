void main(List<String> args) {
  //允许变量运行时可以自由改变类型,var是不允许修改类型的，dynamic是允许修改类型的
  dynamic a = 10;
  a = "hello";
  a = '1.1';
  a = false;
  a = {};
  a = [];
  print(a);
}
