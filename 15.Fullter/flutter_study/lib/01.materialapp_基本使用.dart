import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(
    MaterialApp(
      title: "Flutter初体验", //窗口的标题
      theme: ThemeData(scaffoldBackgroundColor: Colors.red), //整个应用的主题
      home: Scaffold(), //内容骨架屏
    ),
  );
}
