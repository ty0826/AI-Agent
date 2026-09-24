//定制化加载Loading
import 'package:flutter/material.dart';

class LoadingDialog {
  void show(BuildContext context, {String message = '加载中'}) {
    showDialog(
      context: context,
      builder: (context) {
        return Dialog(
          backgroundColor: Colors.transparent,
          child: Center(
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 40, vertical: 20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(10),
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircularProgressIndicator(), //加载动画
                  SizedBox(height: 10),
                  Text(message),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  void hide(BuildContext context) {
    Navigator.pop(context);
  }
}
