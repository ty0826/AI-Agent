import 'package:flutter/material.dart';

void main(List<String> args){
  runApp(const MainPage());
}

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home:Scaffold(
        appBar: AppBar(
          title: Text('column&&row组件的使用',style:TextStyle(color: Colors.white,fontSize: 25)),
          centerTitle: true,
          backgroundColor:Colors.blue,
        ),
        body: Container(
          decoration: BoxDecoration(color: Colors.pink),
          width: double.infinity,
          height: double.infinity,
          // padding: EdgeInsets.all(20),//四周都是20
          // padding: EdgeInsets.only(top: 10,left: 20,right: 20,bottom: 20),
          // padding: EdgeInsets.symmetric(horizontal: 20,vertical: 10),//横向20，纵向10
          // padding: EdgeInsets.fromLTRB(10, 20, 30, 40),//左上右下
          child: Padding(
            padding: EdgeInsets.fromLTRB(10, 20, 30, 40),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,//主轴，垂直方向上
              crossAxisAlignment: CrossAxisAlignment.center,//水平方向
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  crossAxisAlignment:CrossAxisAlignment.center,
                  children: [
                    Container(
                      height: 100,
                      width: 100,
                      color: Colors.blue,
                    ),
                    Container(
                      margin: EdgeInsets.only(left: 10,right: 10),
                      height: 200,
                      width: 200,
                      color: Colors.blue,
                      child:Center(
                        child:Text(
                            'column是垂直排列的，row是水平方向排列的', 
                             style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 20,
                                  )
                              ),
                      )
                    ),
                    Container(
                      height: 100,
                      width: 100,
                      color: Colors.blue,
                    ),
                  ],
                )
              ]
             ))
        ),
      ) ,
    );
  }
}