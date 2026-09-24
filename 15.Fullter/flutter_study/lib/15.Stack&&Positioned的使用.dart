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
            'Stack&&Positioned的使用',
            style: TextStyle(color: Colors.black, fontSize: 25),
          ),
          centerTitle: true,
          backgroundColor: Colors.white,
        ),
        body: Container(
          width: double.infinity,
          height: double.infinity,
          color: Colors.blue,
          child: Stack(
            alignment: Alignment.center,
            children: [
              Container(width: 300, height: 300, color: Colors.red),
              Positioned(
                bottom: 0,
                right: 0,
                child: Container(width: 200, height: 200, color: Colors.pink),
              ),
              Positioned(
                top: 0,
                left: 0,
                child: Container(width: 100, height: 100, color: Colors.amber),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
