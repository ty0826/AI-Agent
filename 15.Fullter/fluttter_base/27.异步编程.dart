void main(List<String> args) {
  Future f = Future(() {
    // return "hello future";
    throw Exception('错误');
  });
  f.then((value) {
    print(value);
  });
  f.catchError((error) {
    print(error);
  });
}
