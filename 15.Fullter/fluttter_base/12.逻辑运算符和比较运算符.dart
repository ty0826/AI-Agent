void main(List<String> args) {
  /**
   * 比较运算符
   * >、<、>=、<=、==、!=,返回的都是boolean类型
   */
  int a = 10;
  int b = 20;
  print(a > b); // false
  print(a < b); // true
  print(a >= b); // false
  print(a <= b); // true
  print(a == b); // false
  print(a != b); // true

  /**
   * 逻辑运算符
   * !、&&、||
   */
  bool c = true;
  bool d = false;
  print(!c); // false
  print(c && d); // false
  print(c || d); // true
}
