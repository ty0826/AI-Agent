void main(List<String> args) {
  int result = add(1, 2);
  print(result);
  int result2 = add2(1, 2, 20, 30);
  print(result2);
  int result1 = add1(1, 2, c: 10, d: 20);
  print(result1);

  test();
}

/**
 * 可选参数，两者不可混用
 * 1.位置可选参数,[String? name,String? school]，调用时可以指定参数名，也可以不指定参数名，但是必须跟在必填参数后面
 * 2.命名可选参数,{String? name}，调用时必须指定参数名
 */
add(int a, int b) {
  return a + b;
}

// 位置可选参数,必须要根据顺序传参
add2(int a, int b, [int? c, int? d]) {
  return a + b + (c ?? 0) + (d ?? 0);
}

// 命名可选参数,{String? name}，调用时必须指定参数名
add1(int a, int b, {int? c, int? d}) {
  return a + b + (c ?? 0) + (d ?? 0);
}

void test() {
  print('测试数据');
}
