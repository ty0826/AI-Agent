import 'package:flutter/material.dart';
import 'package:hm_shop/pages/loginPage/index.dart';
import 'package:hm_shop/pages/mainPage/index.dart';
import 'package:hm_shop/pages/404/index.dart';

class getRootWidget extends StatelessWidget {
  const getRootWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      initialRoute: '/',
      routes: getRouter(),
      onUnknownRoute: (settings) =>
          MaterialPageRoute(builder: (context) => NotFound()),
    );
  }
}

Map<String, Widget Function(BuildContext)> getRouter() {
  return {'/': (context) => mainPage(), '/login': (context) => LoginPage()};
}
