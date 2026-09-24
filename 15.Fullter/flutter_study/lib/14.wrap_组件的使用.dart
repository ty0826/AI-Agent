import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const MainPage());
}

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  List<Widget> getList() {
    return List.generate(
      10,
      (index) => Container(
        width: 100,
        height: 100,
        color: Colors.pink,
        child: Text(index.toString()),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text(
            'wrap组件的使用',
            style: TextStyle(color: Colors.white, fontSize: 25),
          ),
          centerTitle: true,
          backgroundColor: Colors.blue,
        ),
        body: Container(
          color: Colors.amber,
          child: Wrap(
            direction: Axis.horizontal,
            spacing: 11, //水平方向间距
            runSpacing: 10, //垂直方向间距
            alignment: WrapAlignment.spaceAround, //水平方向排列方式
            children: getList(),
          ),
          // decoration: BoxDecoration(color: Colors.pink),
        ),
      ),
    );
  }
}
