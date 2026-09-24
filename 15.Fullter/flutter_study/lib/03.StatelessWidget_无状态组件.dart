import 'package:flutter/material.dart';

void main(List<String> args){
  runApp(const Mainpage());
}

class Mainpage extends StatelessWidget{
  const Mainpage({super.key});

  @override
  Widget build(BuildContext context) { 
    return MaterialApp(
      title: "StatelessWidget--无状态组件使用1",
      home: Scaffold(
        appBar: AppBar(
          title: Text("StatelessWidget--无状态组件使用"),
        ),
        body:Container(
          color: Colors.pink,
          child: Center(
            child: Text('StatelessWidget'),
          ),
        ),
        bottomNavigationBar:SizedBox(
          height: 50,
          child: Center(
            child: Text("无状态组件使用"),
          ),
        ),
      ),
    );
  }
}