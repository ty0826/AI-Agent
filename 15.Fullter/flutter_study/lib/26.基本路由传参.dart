import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const MainPage());
}

//路由跳转---MaterialApp风格，只能有一个MaterialApp
class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(home: ListPage());
  }
}

class ListPage extends StatefulWidget {
  const ListPage({super.key});

  @override
  State<ListPage> createState() => _ListPageState();
}

class _ListPageState extends State<ListPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('基本路由传参---列表页', style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.red,
        centerTitle: true,
      ),
      body: ListView.builder(
        padding: EdgeInsets.all(10),
        itemCount: 50,
        itemBuilder: (BuildContext context, int index) => GestureDetector(
          onTap: () => {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => pageDetail(id: index.toString()),
              ),
            ),
          },
          child: Container(
            alignment: Alignment.center,
            height: 100,
            width: double.infinity,
            decoration: BoxDecoration(color: Colors.blue),
            margin: EdgeInsets.only(top: 10),
            child: Text(
              '第${index + 1}条数据',
              style: TextStyle(color: Colors.white, fontSize: 25),
            ),
          ),
        ),
      ),
    );
  }
}

class pageDetail extends StatefulWidget {
  final String? id;
  const pageDetail({super.key, this.id});

  @override
  State<pageDetail> createState() => _pageDetailState();
}

class _pageDetailState extends State<pageDetail> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('详情页', style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.red,
        centerTitle: true,
      ),
      body: Center(
        child: TextButton(
          onPressed: () => {Navigator.pop(context)},
          child: Text('返回上一页${widget.id}'),
        ),
      ),
    );
  }
}
