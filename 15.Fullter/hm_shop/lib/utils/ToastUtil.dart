import 'package:flutter/material.dart';

class Toastutil {
  static bool Loading = false;
  static void showToast(BuildContext context, String msg) {
    if (Toastutil.Loading) {
      return;
    }
    Toastutil.Loading = true;
    //延时器
    Future.delayed(Duration(seconds: 3), () {
      Toastutil.Loading = false;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        width: 180,
        // margin: EdgeInsets.only(left: 20, right: 20, bottom: 100),
        padding: EdgeInsets.all(5),
        //圆角
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadiusGeometry.circular(30),
        ),
        behavior: SnackBarBehavior.floating, //悬浮
        duration: Duration(seconds: 5),
        content: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Icon(Icons.check_circle, color: Colors.greenAccent, size: 20),
            // SizedBox(width: 10),
            Text(msg, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}
