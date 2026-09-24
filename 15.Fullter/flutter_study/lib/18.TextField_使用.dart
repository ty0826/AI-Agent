import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const MainPage());
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  final TextEditingController _username = TextEditingController();
  final TextEditingController _passward = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("登录"), centerTitle: true),
        body: Container(
          decoration: BoxDecoration(
            color: const Color.fromARGB(255, 107, 114, 218),
          ),
          child: Padding(
            padding: EdgeInsets.all(10),
            child: Column(
              children: [
                TextField(
                  controller: _username,
                  onChanged: (value) => {print('$value---值变化')},
                  onSubmitted: (value) => {print('$value---提交')},
                  decoration: InputDecoration(
                    contentPadding: EdgeInsets.only(left: 20), //内容内边距
                    hintText: "请输入账号",
                    fillColor: Colors.amber, //输入框背景色
                    filled: true, //是否显示背景色
                    border: OutlineInputBorder(
                      borderSide: BorderSide.none,
                      borderRadius: BorderRadius.circular(25),
                    ),
                  ),
                ),
                SizedBox(height: 20),
                TextField(
                  controller: _passward,
                  obscureText: true, //不显示实际内容
                  decoration: InputDecoration(
                    contentPadding: EdgeInsets.only(left: 20),
                    hintText: '请输入密码',
                    fillColor: Colors.amber,
                    filled: true,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(25),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
                SizedBox(height: 20),
                Container(
                  width: double.infinity,
                  height: 50,
                  decoration: BoxDecoration(
                    color: Colors.black,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: TextButton(
                    onPressed: () => {
                      print('账号${_username.text},密码${_passward.text}'),
                    },
                    child: Text(
                      '登录',
                      style: TextStyle(color: Colors.white, fontSize: 20),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
