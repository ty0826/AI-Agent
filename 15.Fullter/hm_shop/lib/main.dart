import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:hm_shop/routes/index.dart';
import 'package:hm_shop/stores/UserInfoController.dart';

void main() {
  // 全局注册 UserInfoController
  Get.put(UserInfoController());

  runApp(const getRootWidget());
}
