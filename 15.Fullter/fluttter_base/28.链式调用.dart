void main(List<String> args) {
  /**
   * Future().then()拿到执行成功的结果
   * 上一个then返回的对象会在下一个then中接收
   * FUture.catchError()拿到执行失败的结果
   */
  Future f = Future(() {
    return 'Hello world';
  });
  f
      .then((value) {
        return Future(() => 'task');
      })
      .then((value) {
        return Future(() => '$value-task1');
      })
      .then((value) {
        return Future(() => '$value-task2');
      })
      .then((value) {
        print(value);
      })
      .catchError((onError) {
        print(onError);
      });
}
