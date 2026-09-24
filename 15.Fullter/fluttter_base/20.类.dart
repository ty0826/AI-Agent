void main(List<String> args) {
  Personal people = Personal(name: '张三', age: 20, sex: '男');
  people.printInfo();
  Personal people1 = Personal.createPersonal(name: '李四', age: 20, sex: '男');
  people1.printInfo();
}

class Personal {
  String name;
  int? age;
  String? sex;
  // 默认构造函数
  // Personal({String? name, int? age, String? sex}) {
  //   this.name = name;
  //   this.age = age;
  //   this.sex = sex;
  // }
  // 默认构造函数--语法糖
  Personal({required this.name, this.age, this.sex});
  //  Personal(this.name, this.age, this.sex);---》Personal people = Personal(  '张三',  20,  '男');
  // 命名构造函数
  // Personal.createPersonal({String? name, int? age, String? sex}) {
  //   this.name = name;
  //   this.age = age;
  //   this.sex = sex;
  // }
  // 命名构造函数--语法题
  Personal.createPersonal({required this.name, this.age, this.sex});
  void printInfo() {
    print('name: $name, age: $age, sex: $sex');
  }
}
