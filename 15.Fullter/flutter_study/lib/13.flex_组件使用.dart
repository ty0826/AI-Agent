import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const MainPage());
}

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text(
            'flex组件的使用',
            style: TextStyle(color: Colors.white, fontSize: 25),
          ),
          centerTitle: true,
          backgroundColor: Colors.blue,
        ),
        body: SizedBox(
          // decoration: BoxDecoration(color: Colors.pink),
          width: double.infinity,
          height: double.infinity,
          // padding: EdgeInsets.all(20),//四周都是20
          // padding: EdgeInsets.only(top: 10,left: 20,right: 20,bottom: 20),
          // padding: EdgeInsets.symmetric(horizontal: 20,vertical: 10),//横向20，纵向10
          // padding: EdgeInsets.fromLTRB(10, 20, 30, 40),//左上右下
          child: Flex(
            direction: Axis
                .horizontal, //horizontal水平方向，vertical垂直方向，expended会撑满剩余空间，Flexible只会按照实际宽高占据
            children: [
              Expanded(
                flex: 1,
                child: Container(
                  decoration: BoxDecoration(color: Colors.blue),
                  height: 100,
                  width: 100,
                ),
              ),
              Flexible(
                flex: 2,
                fit: FlexFit.tight,
                child: Container(
                  decoration: BoxDecoration(color: Colors.red),
                  width: 100,
                  height: 100,
                ),
              ),
              Expanded(
                flex: 1,
                child: Container(
                  decoration: BoxDecoration(color: Colors.green),
                  width: 100,
                  height: 100,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
