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
            'Image的使用',
            style: TextStyle(color: Colors.black, fontSize: 25),
          ),
          centerTitle: true,
          backgroundColor: Colors.white,
        ),
        body: Center(
          // child: Image.asset(
          //   "lib/images/icon.png",
          //   width: 100,
          //   height: 100,
          //   fit: BoxFit.contain,
          // ),
          child: Image.network(
            'https://gips3.baidu.com/it/u=3886271102,3123389489&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960',
            width: 500,
            height: 500,
            fit: BoxFit.cover,
          ),
        ),
      ),
    );
  }
}
