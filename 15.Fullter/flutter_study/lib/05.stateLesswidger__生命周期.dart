import 'package:flutter/material.dart';

void main(List<String> args){
  runApp(const MainPage());
}

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override //在无状态组件的生命周期里，当组件被创建或者父组件状态发生变化都会调用build()方法
  Widget build(BuildContext context) {
    print('无状态组件的构建执行');
    return  MaterialApp(  
      home: Scaffold(
        appBar: AppBar(
          title: Text('StatelessWidget--无状态组件使用'),
        ),
        body:Container(
          color: Colors.amber,
          child: Center(
            child: Text('无状态组件'),
          ),
        )
      ),
      );
  }
}