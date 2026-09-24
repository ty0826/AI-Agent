/**
 * 在不使用传统继承的情况下，向类中添加新的功能
 * minxin关键词定义一个对象
 * 使用with将定义的对象混入到当前对象
 * 一个类支持with多个mixin，遵循后来居上，前面会被覆盖
 */
void main(List<String> args) {
  Teacher teacher = Teacher('小明', 20);
  teacher.song(teacher.name!); //teacher.name!,确保这个不是null
}

//定义一个对象
mixin Base {
  void song(String name) {
    print('$name在唱歌');
  }
}

class Student with Base {
  String? name;
  int? age;
  Student(this.name, this.age);
}

class Teacher with Base {
  String? name;
  int? age;
  Teacher(this.name, this.age);
}
