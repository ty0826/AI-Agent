void main(List<String> args) {
  add();
  OnAdd(add());
}

// 声明一个匿名函数赋值的add变量
Function add = () {
  print("匿名函数");
};

void OnAdd(Function callBack) {
  callBack();
}
