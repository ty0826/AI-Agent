import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(
    MaterialApp(
      title: "Flutter初体验", //窗口的标题
      theme: ThemeData(scaffoldBackgroundColor: Colors.blue), //整个应用的主题
      home: Scaffold(
        appBar: AppBar(
          title: Text('头部标题')
          ),
        body: Container(
          color:Colors.pink,
          child: Center(
            child: Text('主体内容')
            )
          ),
        bottomNavigationBar: SizedBox(
          height: 80,
          child: Center(
            child: Text('底部内容')
            ),
        ),
      ), //内容骨架屏
    ),
  );
}
