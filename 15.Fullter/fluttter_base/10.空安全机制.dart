void main(List<String> args) {
  //运行编译静态检查时将运行空指针提前暴露出来，避免空指针异常
  String? user_name = null; //? 表示name可以为空
  user_name?.startsWith("张"); //编译时会报错，提示空指针异常
  user_name!.startsWith("张"); //编译时不会报错，提示空指针异常，非空断言
  String displayname = user_name ?? "张三"; //??表示如果user_name为空，则使用默认值
  print(displayname);
}
