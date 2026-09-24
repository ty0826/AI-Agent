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
  final ScrollController _scorllView = ScrollController();
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('SingleChildScrollView滚动'),
          centerTitle: true,
        ),
        body: Stack(
          children: [
            SingleChildScrollView(
              controller: _scorllView,
              child: Column(
                children: List.generate(
                  100,
                  (index) => Container(
                    margin: EdgeInsets.all(10),
                    width: double.infinity,
                    height: 50,
                    decoration: BoxDecoration(color: Colors.blue),
                    child: Center(
                      child: Text(
                        '第${index + 1}条数据',
                        style: TextStyle(color: Colors.white, fontSize: 20),
                      ),
                    ),
                  ),
                ),
              ),
            ),
            Positioned(
              top: 0,
              right: 10,
              child: GestureDetector(
                onTap: () => {
                  _scorllView.animateTo(
                    0,
                    duration: Duration(seconds: 1),
                    curve: Curves.easeIn,
                  ),
                },
                child: Container(
                  width: 50,
                  height: 50,
                  decoration: BoxDecoration(
                    color: Colors.red,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Center(
                    child: Text(
                      '去顶部',
                      style: TextStyle(fontSize: 16, color: Colors.white),
                    ),
                  ),
                ),
              ),
            ),
            Positioned(
              bottom: 10,
              right: 10,
              child: GestureDetector(
                onTap: () => {
                  _scorllView.animateTo(
                    _scorllView.position.maxScrollExtent,
                    duration: Duration(seconds: 1),
                    curve: Curves.easeIn,
                  ),
                },
                child: Container(
                  width: 50,
                  height: 50,
                  decoration: BoxDecoration(
                    color: Colors.red,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Center(
                    child: Text(
                      '去底部',
                      style: TextStyle(fontSize: 16, color: Colors.white),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
