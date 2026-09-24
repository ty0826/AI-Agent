import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const MainPage());
}

//路由跳转---MaterialApp风格，只能有一个MaterialApp
class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      initialRoute: '/list', //首次展示页面
      routes: {
        "/list": (context) => ListPage(),
        '/list_detail': (context) => pageDetail(),
      },
      home: ListPage(),
    );
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
        title: Text('命名路由传参---列表页', style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.red,
        centerTitle: true,
      ),
      body: ListView.builder(
        padding: EdgeInsets.all(10),
        itemCount: 50,
        itemBuilder: (BuildContext context, int index) => GestureDetector(
          onTap: () => {
            // Navigator.push(
            //   context,
            //   MaterialPageRoute(builder: (context) => pageDetail()),
            // ),
            Navigator.pushNamed(
              context,
              '/list_detail',
              arguments: {'id': index + 1},
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
  const pageDetail({super.key});

  @override
  State<pageDetail> createState() => _pageDetailState();
}

/// 基础路由传参，跟父子组件通信模式一样，父路由{id:index},子路由里面weight.id
/// 命名路由传参，父路由需要{  arguments: {'id': index + 1},},子路由需要在initState的Future.microtask方法才能拿到，具体方法是ModalRoute.of(context).setting.arguments['id']
///
class _pageDetailState extends State<pageDetail> {
  String _id = '';
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    //initState获取不到参数，需要在Future.microtask才能拿到
    Future.microtask(() {
      if (ModalRoute.of(context) != null) {
        Map<String, dynamic> params =
            ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
        _id = params["id"].toString();
        setState(() {});
      }
    });
  }

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
          onPressed: () => {
            // Navigator.pop(context)
            Navigator.pushNamed(context, '/list'),
          },
          child: Text('返回上一页$_id'),
        ),
      ),
    );
  }
}
