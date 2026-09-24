void main(List<String> args) {
  Personal p = Personal('张三', 23, '女');
  p._study(); //Dart类的私有属性是文件级别的，不同文件调用__study会报错
}

class Personal {
  String name;
  int age;
  String sex;

  Personal(this.name, this.age, this.sex);
  void study() {
    _study();
  }

  void _study() {
    print("name:$name,age:${age},sex:$sex");
  }
}
