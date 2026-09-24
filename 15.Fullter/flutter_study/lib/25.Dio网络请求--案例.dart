import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import './Dio_request.dart';

void main(List<String> args) {
  runApp(const MainPage());
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  List<Map<String, dynamic>> _list = [];
  @override
  void initState() {
    super.initState();
    _getData();
  }

  void _getData() async {
    DioUtils request = DioUtils();
    Response<dynamic> result = await request.get(
      'https://geek.itheima.net/v1_0/channels',
    );
    Map<String, dynamic> res =
        result.data as Map<String, dynamic>; //整体返回的是Map<String, dynamic>
    List data = res["data"]["channels"] as List;
    _list = data.cast<Map<String, dynamic>>(); //将数据按照Map<String, dynamic>处理
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Dio网络请求--案例', style: TextStyle(color: Colors.white)),
          centerTitle: true,
          backgroundColor: Colors.red,
        ),
        body: GridView.builder(
          padding: EdgeInsets.all(10),
          itemCount: _list.length,
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
            childAspectRatio: 2 / 3,
          ),
          itemBuilder: (BuildContext context, int index) =>
              childItem(item: _list[index]),
        ),
      ),
    );
  }
}

class childItem extends StatelessWidget {
  final Map<String, dynamic> item;
  const childItem({super.key, required this.item});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(color: Colors.red),
      child: Text(item['name'], style: TextStyle(color: Colors.white)),
    );
  }
}
