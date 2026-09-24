import 'package:flutter/material.dart';

void main(List<String> args){
  runApp(const MainPage());
}

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home:Scaffold(
        appBar: AppBar(
          title: Text('padding组件的使用',style:TextStyle(color: Colors.white,fontSize: 25)),
          centerTitle: true,
          backgroundColor:Colors.blue,
        ),
        body: Container(
          decoration: BoxDecoration(color: Colors.pink),
          // padding: EdgeInsets.all(20),//四周都是20
          // padding: EdgeInsets.only(top: 10,left: 20,right: 20,bottom: 20),
          // padding: EdgeInsets.symmetric(horizontal: 20,vertical: 10),//横向20，纵向10
          // padding: EdgeInsets.fromLTRB(10, 20, 30, 40),//左上右下
          child: Padding(
            padding: EdgeInsets.fromLTRB(10, 20, 30, 40),
            child: Container(
            color: Colors.amber,
          ),)
        ),
      ) ,
    );
  }
}