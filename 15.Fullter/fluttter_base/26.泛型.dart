void main(List<String> args) {
  getValue<String>('1');
  printList<String>(['1', '2']);
  Student<String> s = Student();
  s.name = '1';
}

// 泛型方法
T getValue<T>(T value) {
  return value;
}

// 泛型集合
void printList<T>(List<T> list) {
  for (var i = 0; i < list.length; i++) {
    print(list[i]);
  }
}

// 泛型类
class Student<T> {
  T? name;
}
