import 'package:flutter/material.dart';

void main(List<String> args){
  runApp(const MainPage());
}

// 有状态组件 第一个类--对外
class MainPage extends StatefulWidget{
  const MainPage({super.key});

  @override
  State<StatefulWidget> createState() { 
    // return 返回第二个组件
    return _MainPage();
  }
}
class _MainPage extends State<MainPage>{
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title:'StatefulWidget---有状态组件',
      home:Scaffold(
        appBar: AppBar(
          title: Text('StatefulWidget---有状态组件'),
        ),
        body:Container(
          color: Colors.red,
          child: Center(
            child: Text('StatefulWidget'),
          ),
        ),
        bottomNavigationBar: SizedBox(
          height: 50,
          child: Center(
            child: Text('有状态组件使用'),
          ),
        ),
      )
    );
  }
}