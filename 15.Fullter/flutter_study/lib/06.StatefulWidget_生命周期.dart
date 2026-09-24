import 'package:flutter/material.dart';

void main(List<String> args){
  runApp(const MainPage());
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() {
    print('Widget初始化调用');
    return _MainPageState();
  }
}

class _MainPageState extends State<MainPage> {
  @override
  void initState() {
    print('initState执行阶段');
    super.initState();
  }
  @override
  void didChangeDependencies() {
    print('didChangeDependencies执行阶段');
    // TODO: implement didChangeDependencies
    super.didChangeDependencies();
  }
  @override
  void didUpdateWidget(covariant MainPage oldWidget) {
    print('didUpdateWidget执行阶段');
    // TODO: implement didUpdateWidget
    super.didUpdateWidget(oldWidget);
  }
  @override
  void deactivate() {
    print('deactivate执行阶段');
    // TODO: implement deactivate
    super.deactivate();
  }
  @override
  void dispose() {
    print('dispose执行阶段');
    // TODO: implement dispose
    super.dispose();
  }
  @override
  Widget build(BuildContext context) {
    print('build执行阶段');
    return Container();
  }
}


/**
 * 无状态组件-----》build
 * 有状态组件：
 *    1、创建阶段：
*                createState:Widget初始化调用，创建State对象
*                initState:State对象插入Widget树立刻执行，仅执行一次
*                disChangeDependencies:initState后立刻执行，当依赖的InheritedWidget更新时调用，可能会多次
*                build:构建UI方法，初始化或更新后多次调用
 *    2、更新阶段：
 *              didupdateWidget:父组件传入新配置时调用，用于比较新旧配置didupdateWidget-》build
 *    3、销毁阶段:
 *              deactiveate:当State对象从树中暂时移除时调用
 *              dispose:当State对象被永久移除时调用，释放资源
 *    4、仅执行一次的函数：createState,initState,dispose
 *    5、InheritedWidget：专门用于在Widget树中自顶向下高效的共享数据，顶层数据提供数据，子孙节点直接获取
 *        
 * 
 * 
 */