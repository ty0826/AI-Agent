import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const MainPage());
}

// class MainPage extends StatefulWidget {
//   const MainPage({super.key});

//   @override
//   State<MainPage> createState() => _MainPageState();
// }

// class _MainPageState extends State<MainPage> {
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       home: Scaffold(
//         appBar: AppBar(
//           title: Text('组件间通信', style: TextStyle(color: Colors.white)),
//           centerTitle: true,
//           backgroundColor: Colors.red,
//         ),
//         body: Container(
//           alignment: Alignment.center,
//           child: Column(
//             mainAxisAlignment: MainAxisAlignment.center,
//             children: [
//               Text('父组件', style: TextStyle(color: Colors.blue, fontSize: 20)),
//               ChindLess(messages: '父传子--无状态组件'),
//               ChindFull(messages: '父传子--有状态组件'),
//             ],
//           ),
//         ),
//       ),
//     );
//   }
// }

// /// 子组件接受的参数必须要用final定义
// /// 有状态组件需要用widget才能拿到
// ///
// //无状态组件
// class ChindLess extends StatelessWidget {
//   final String? messages;
//   const ChindLess({super.key, this.messages});

//   @override
//   Widget build(BuildContext context) {
//     return Text('子组件$messages');
//   }
// }

// //有状态组件
// class ChindFull extends StatefulWidget {
//   final String messages;
//   const ChindFull({super.key, required this.messages});

//   @override
//   State<ChindFull> createState() => _ChindFullState();
// }

// class _ChindFullState extends State<ChindFull> {
//   @override
//   Widget build(BuildContext context) {
//     return Text('子组件${widget.messages}');
//   }
// }

// 案例
class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => __MainPageStateState();
}

class __MainPageStateState extends State<MainPage> {
  List<String> list = ['鱼香肉丝', '宫保鸡丁', '麻婆豆腐', '香干肉丝'];
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('父子组件通信', style: TextStyle(color: Colors.white)),
          backgroundColor: Colors.red,
          centerTitle: true,
        ),
        body: GridView.count(
          padding: EdgeInsets.all(10),
          crossAxisCount: 2,
          mainAxisSpacing: 10,
          crossAxisSpacing: 10,
          children: List.generate(
            list.length,
            (index) => Child(
              name: list[index],
              index: index,
              handleDelete: (value) => {
                setState(() {
                  list.removeAt(index);
                }),
              },
            ),
          ),
        ),
      ),
    );
  }
}

class Child extends StatefulWidget {
  final String name;
  final int index;
  final Function(int index) handleDelete;
  const Child({
    super.key,
    required this.name,
    required this.index,
    required this.handleDelete,
  });

  @override
  State<Child> createState() => _ChildState();
}

class _ChildState extends State<Child> {
  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          alignment: Alignment.center,
          decoration: BoxDecoration(color: Colors.blue),
          child: Text(
            widget.name,
            style: TextStyle(color: Colors.white, fontSize: 20),
          ),
        ),
        Positioned(
          top: 10,
          right: 10,
          child: IconButton(
            onPressed: () => {widget.handleDelete(widget.index)},
            icon: Icon(Icons.delete, color: Colors.red),
          ),
        ),
      ],
    );
  }
}
