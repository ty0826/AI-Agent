import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const MianPage());
}

class MianPage extends StatelessWidget {
  const MianPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          backgroundColor:Color(0xffe0e7ff),
          title: Text("Container&&center组件用法"),
          centerTitle: true,
        ),
        body: Center(
          child: Container(
          margin: EdgeInsets.all(20),
          padding: EdgeInsets.all(10),
          height: 200,
          width: 200,
          decoration:BoxDecoration(
            color: const Color.fromARGB(255, 184, 33, 243),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(width: 3,color: Colors.amber)
          ),
          transform: Matrix4.rotationZ(0.05),
          // alignment: Alignment.center,
          child: Center(
            child: Text(
              "hello Container",
              style: TextStyle(color: Colors.white,fontSize: 20)),
          ),
          )
        )
        ),
    );
  }
}
