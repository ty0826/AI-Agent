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
        appBar: AppBar(title: Text('GridView二维网格布局滚动'), centerTitle: true),
        // GridView.extent自适应列展示，GridView.count固定列展示，GridView.builder懒加载
        body: GridView.builder(
          itemCount: 100,
          padding: EdgeInsets.all(10),
          // SliverGridDelegateWithFixedCrossAxisCount, 一行展示个数
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 4,
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
            childAspectRatio: 2, //宽高比 宽/高=2
          ),
          //SliverGridDelegateWithMaxCrossAxisExtent设置主轴高度和交叉轴的宽度
          // gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
          //   maxCrossAxisExtent: 200, //宽度
          //   mainAxisExtent: 100, //高度
          //   mainAxisSpacing: 10,
          //   crossAxisSpacing: 10,
          // ),
          itemBuilder: (BuildContext context, int index) => Container(
            alignment: Alignment.center,
            decoration: BoxDecoration(color: Colors.amber),
            child: Text('第${index + 1}个'),
          ),
        ),

        // body: GridView.extent(
        //   padding: EdgeInsets.all(10),
        //   mainAxisSpacing: 10,
        //   crossAxisSpacing: 10,
        //   maxCrossAxisExtent: 200, //最大宽度设置
        //   mainAxisExtent: 100, //固定高度设置
        //   children: List.generate(
        //     100,
        //     (int index) => Container(
        //       alignment: Alignment.center,
        //       decoration: BoxDecoration(color: Colors.amber),
        //       child: Text('第${index + 1}个'),
        //     ),
        //   ),
        // ),

        //
        // body: GridView.count(
        //   // scrollDirection: Axis.horizontal, //改变主轴方向
        //   padding: EdgeInsets.all(10),
        //   crossAxisCount: 3, //一行展示几个
        //   mainAxisSpacing: 10,
        //   crossAxisSpacing: 10,
        //   children: List.generate(
        //     100,
        //     (int index) => Container(
        //       alignment: Alignment.center,
        //       width: 100,
        //       height: 100,
        //       decoration: BoxDecoration(color: Colors.amber),
        //       child: Text(
        //         '第${index + 1}个',
        //         style: TextStyle(color: Colors.white, fontSize: 20),
        //       ),
        //     ),
        //   ),
        // ),
      ),
    );
  }
}
