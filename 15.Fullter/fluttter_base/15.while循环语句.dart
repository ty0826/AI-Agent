void main(List<String> args) {
  //break:跳过整个循环，continue:跳过本次循环,进入下一次循环
  int i = 0;
  while (i < 10) {
    if (i == 5) {
      i++;
      continue;
    }
    print(i);
    i++;
  }
  int j = 0;
  while (j < 10) {
    if (j == 5) {
      break;
    }
    print(j);
    j++;
  }
}
