import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:hm_shop/stores/UserInfoController.dart';

class CartView extends StatefulWidget {
  const CartView({super.key});

  @override
  State<CartView> createState() => _CartViewState();
}

class _CartViewState extends State<CartView> {
  final UserInfoController _userInfoController = Get.find();
  @override
  Widget build(BuildContext context) {
    return Obx(() {
      return Center(
        child: Text('购物车${_userInfoController.user.value.cityCode}'),
      );
    });
  }
}
