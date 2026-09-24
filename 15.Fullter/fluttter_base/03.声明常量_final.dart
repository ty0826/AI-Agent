/**
 * final是指在运行时才确定的值，后面不允许修改，
 * const是指在编译时就确定的值，后面不允许修改
 */
void main(List<String> args) {
  final age = DateTime.now();
  print(age);
}
