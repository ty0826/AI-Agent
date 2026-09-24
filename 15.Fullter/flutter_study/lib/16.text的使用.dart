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
            'text的使用',
            style: TextStyle(color: Colors.black, fontSize: 25),
          ),
          centerTitle: true,
          backgroundColor: Colors.white,
        ),
        body: Container(
          width: double.infinity,
          height: double.infinity,
          color: Colors.blue,
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  'hello fluttter!',
                  style: TextStyle(
                    fontSize: 20,
                    color: Colors.amber,
                    fontWeight: FontWeight.bold,
                    fontStyle: FontStyle.italic,
                    decoration: TextDecoration.underline,
                    decorationColor: Colors.redAccent,
                  ),
                ),
                Text(
                  '今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错，今天天气非常不错',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis,
                ),
                Text.rich(
                  TextSpan(
                    text: 'Flutter',
                    style: TextStyle(fontSize: 35, color: Colors.red),
                    children: [
                      TextSpan(
                        text: '不同样式',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Colors.greenAccent,
                        ),
                      ),
                      TextSpan(text: '！'),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
