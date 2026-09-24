import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const mainPage());
}

class mainPage extends StatelessWidget {
  const mainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      initialRoute: '/goodList',
      routes: {"/goodList": (context) => goodList()}, //找不到路由是会进入onGenerateRoute
      onGenerateRoute: (settings) {
        if (settings.name == '/cartList') {
          bool isLogin = true;
          if (isLogin) {
            return MaterialPageRoute(builder: (context) => carPage());
          } else {
            return MaterialPageRoute(builder: (context) => loginPage());
          }
        }
        return null;
      },
      onUnknownRoute: (setting) {
        return MaterialPageRoute(builder: (context) => NotFound());
      },
    );
  }
}

class goodList extends StatefulWidget {
  const goodList({super.key});

  @override
  State<goodList> createState() => _goodListState();
}

class _goodListState extends State<goodList> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('商品列表')),
      body: Container(
        child: TextButton(
          onPressed: () => {Navigator.pushNamed(context, 'qqq')},
          child: Text('跳转'),
        ),
      ),
    );
  }
}

class carPage extends StatefulWidget {
  const carPage({super.key});

  @override
  State<carPage> createState() => _carPageState();
}

class _carPageState extends State<carPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('购物车列表')));
  }
}

class loginPage extends StatefulWidget {
  const loginPage({super.key});

  @override
  State<loginPage> createState() => _loginPageState();
}

class _loginPageState extends State<loginPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('登录页列表')));
  }
}

class NotFound extends StatefulWidget {
  const NotFound({super.key});

  @override
  State<NotFound> createState() => _NotFoundState();
}

class _NotFoundState extends State<NotFound> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('404列表')));
  }
}
