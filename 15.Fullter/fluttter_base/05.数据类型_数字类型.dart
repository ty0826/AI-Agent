void main(List<String> args) {
  /**
   * int:整型数字,toInt()方法将数字类型转换为整型
   * num:数字类型，包含整型和浮点型
   * double:浮点型数字,toDouble()方法将数字类型转换为浮点型
   */
  int age = 10; //声明整型变量
  print(age);
  num weight = 20.5; //声明数字类型变量
  print(weight);
  num score = 99; //声明数字类型变量
  print(score);
  double height = 1.75; //声明浮点型变量
  print(height);
  print('我的年龄是${age}岁,体重是$weight kg,身高是${height}m');
  print(weight is int); //判断weight是否是double类型
  weight = age.toDouble(); //将整型变量age转换为浮点型变量
  height = weight.toDouble(); //将数字类型变量weight转换为浮点型变量
  age = score.toInt(); //将数字类型变量score转换为整型变量
  weight = height; //将浮点型变量height转换为整型变量
}
