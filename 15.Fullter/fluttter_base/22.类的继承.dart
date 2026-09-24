void main(List<String> args) {
  Child child = Child('小明', 18, '男');
  child.decripet();
}

class Parent {
  String? name;
  int age;

  Parent(this.name, this.age);

  void decripet() {
    print('我是$name，今年$age');
  }
}

/**
 * 子类可通过@override重写父类方法
 * 子类不会继承父类的构造函数，必须要使用super关键词调用父类构造函数
 * super语法：子类构造函数（可选命名参数）:super(参数)
 */
class Child extends Parent {
  String sex;
  Child(String? name, int age, this.sex) : super(name, age);
  @override //重写父类方法
  void decripet() {
    super.decripet();
    print('我是$name，今年$age，性别$sex');
  }
}
