void main(List<String> args) {
  //break:跳出整个循环，continue:跳出本次循环，继续下一次循环
  for (int i = 0; i < 10; i++) {
    if (i == 5) {
      continue;
    }
    print(i);
  }
}
