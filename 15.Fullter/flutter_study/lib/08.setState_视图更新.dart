import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const MainPage());
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int count = 0;
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("setState事件")),
        body: Container(
          child: Row(
            children: [
              TextButton(
                onPressed: () => {
                  setState(() {
                    count = count + 1;
                  }),
                },
                child: Text('加'),
              ),
              Text(count.toString()),
              TextButton(
                onPressed: () => {
                  setState(() {
                    count -= 1;
                  }),
                },
                child: Text('减'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
