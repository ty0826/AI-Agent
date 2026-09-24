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
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('ListView滚动'), centerTitle: true),

        //列表长度 builder可以实现懒加载，性能优异，separated具备分割线
        // body: ListView.separated(
        //   itemBuilder: (BuildContext context, int index) {
        //     return Container(
        //       margin: EdgeInsets.all(10),
        //       width: double.infinity,
        //       height: 50,
        //       decoration: BoxDecoration(color: Colors.blue),
        //       alignment: Alignment.center,
        //       child: Text(
        //         '第${index + 1}条数据',
        //         style: TextStyle(color: Colors.white, fontSize: 20),
        //       ),
        //     );
        //   },
        //   separatorBuilder: (BuildContext context, int index) {
        //     return Padding(
        //       padding: EdgeInsets.all(10),
        //       child: Container(
        //         height: 10,
        //         width: double.infinity,
        //         decoration: BoxDecoration(color: Colors.amber),
        //       ),
        //     );
        //   },
        //   itemCount: 1000,
        // ),

        //
        // body: ListView.builder(
        //   itemCount: 100,
        //   padding: EdgeInsets.all(10),
        //   itemBuilder: (BuildContext context, int index) {
        //     return Container(
        //       margin: EdgeInsets.all(10),
        //       width: double.infinity,
        //       height: 50,
        //       decoration: BoxDecoration(color: Colors.blue),
        //       alignment: Alignment.center,
        //       child: Text(
        //         '第${index + 1}条数据',
        //         style: TextStyle(color: Colors.white, fontSize: 20),
        //       ),
        //     );
        //   },

        // ),
        body: ListView(
          children: List.generate(
            100,
            (index) => Container(
              margin: EdgeInsets.all(10),
              width: double.infinity,
              height: 50,
              decoration: BoxDecoration(color: Colors.blue),
              alignment: Alignment.center,
              child: Text(
                '第${index + 1}条数据',
                style: TextStyle(color: Colors.white, fontSize: 20),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
