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
          title: Text('Align组件的使用',style:TextStyle(color: Colors.white,fontSize: 25)),
          centerTitle: true,
          backgroundColor:Colors.blue,
        ),
        body: Container(
          color: Colors.pink,
          child: Align(
            alignment: Alignment.centerLeft,//将子组件对齐到父组件
            widthFactor: 1,//Align的宽度是子组件的1倍
            heightFactor: 2,//Align的高度是子组件的2倍
            child: Icon(Icons.star,size:150,color: Colors.amberAccent)
          ),
        ),
      ) ,
    );
  }
}