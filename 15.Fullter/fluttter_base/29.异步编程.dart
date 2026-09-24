void main(List<String> args) {
  test();
}

void test() async {
  try {
    // await Future(() {
    //   print('测试');
    // });
    await Future.delayed(Duration(seconds: 3));
    throw Exception();
  } catch (error) {
    print(error);
  }
}
