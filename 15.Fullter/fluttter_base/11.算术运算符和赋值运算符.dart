void main(List<String> args) {
  /**
   * 算术运算符：+、-、*、/、~/、%
   */
  double a = 30.25;
  int b = 20;
  num c = a + b;
  print(c);
  double d = a - b;
  print(d);
  double e = a * b;
  print(e);
  double f = a / b;
  print(f);
  num g = a ~/ b; //取整除
  print(g);
  double h = a % b; //取余
  print(h);

  /**
   * 赋值运算符：=、+=、-=、*=、/=、~/=、%=
   */
  num i = 10;
  i += 5; //i = i + 5
  print(i);

  i -= 3; //i = i - 3
  print(i);

  i *= 2; //i = i * 2
  print(i);

  i /= 4; //i = i / 4
  print(i);

  i ~/= 3; //i = i ~/ 3
  print(i);

  i %= 4; //i = i % 4
  print(i);
}
