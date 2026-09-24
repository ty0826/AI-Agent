import 'package:flutter/material.dart';

void main(List<String> args){
  runApp(const MainPage());
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title:'点击事件',
      // theme: ThemeData(scaffoldBackgroundColor: ),
      home: Scaffold(
        appBar: AppBar(
          title: Text("flutter点击事件"),
        ),
        body: Container(
          color: Colors.red,
          child: Center(
              child: TextButton(
                onPressed: ()=>{
                  print('点击')
                },
                child: Text('中间区域')
              ),
          ),
          // child: Center(
          //  child: GestureDetector(
          //     child: Text('中间区域'),
          //     onTap: ()=>{
          //       print('点击了区域')
          //     },
          //  ),
          // ),
        ),
        bottomNavigationBar: SizedBox(
          height: 50,
          child: Center(
            child: Text('底部'),
          ),
        ),
      ),
    );
  }
}
/**
 * 组件自带的点击事件：
 *  ElevateButton，TextButton,OutlineBUtton,FloatingActionButton--->onpresse方法
 * GestureDetector()可以自定义点击事件
 */