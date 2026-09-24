//声明常量 const
void main(List<String> args) {
  const age = 10; //const声明常量之后， 并且不允许有变量值
  print(age);

  const weight = 20; //var声明变量之后，后面类型不允许修改
  const math = weight + age + 10; //const声明常量之后， 并且不允许有变量值(用var声明也不行)
  print(math);
}
