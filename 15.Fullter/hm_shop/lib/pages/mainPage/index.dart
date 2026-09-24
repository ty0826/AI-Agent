import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:hm_shop/api/login.dart';
import 'package:hm_shop/pages/home/index.dart';
import 'package:hm_shop/pages/category/index.dart';
import 'package:hm_shop/pages/cart/index.dart';
import 'package:hm_shop/pages/personal/index.dart';
import 'package:hm_shop/stores/UserInfoController.dart';
import 'package:hm_shop/stores/tokenManmager.dart';

class mainPage extends StatefulWidget {
  const mainPage({super.key});

  @override
  State<mainPage> createState() => _mainPageState();
}

final List<Map<String, String>> _tableList = [
  {
    "icon": "lib/assets/ic_public_home_normal.png",
    "acvtive": "lib/assets/ic_public_home_active.png",
    "label": "首页",
  },
  {
    "icon": "lib/assets/ic_public_pro_normal.png",
    "acvtive": "lib/assets/ic_public_pro_active.png",
    "label": "分类",
  },
  {
    "icon": "lib/assets/ic_public_cart_normal.png",
    "acvtive": "lib/assets/ic_public_cart_active.png",
    "label": "购物车",
  },
  {
    "icon": "lib/assets/ic_public_my_normal.png",
    "acvtive": "lib/assets/ic_public_my_active.png",
    "label": "我的",
  },
];

List<BottomNavigationBarItem> _getTabBarWidget() {
  return List.generate(_tableList.length, (int index) {
    return BottomNavigationBarItem(
      icon: Image.asset(_tableList[index]['icon']!, width: 30, height: 30),
      activeIcon: Image.asset(
        _tableList[index]['acvtive']!,
        width: 30,
        height: 30,
      ),
      label: _tableList[index]['label'],
    );
  });
}

List<Widget> _getchindren() {
  return [HomeView(), CategoryView(), CartView(), PersonalView()];
}

class _mainPageState extends State<mainPage> {
  int _currentIndex = 0;
  final UserInfoController _userInfoController = Get.find<UserInfoController>();
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _initUserinfo();
  }

  void _initUserinfo() async {
    await tokenManmager.init();
    if (tokenManmager.getToken().isNotEmpty) {
      _userInfoController.updateUserInfo(await userInfoApi());
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      //SafeArea避开安全区组件,渲染子路由
      body: IndexedStack(index: _currentIndex, children: _getchindren()),
      bottomNavigationBar: BottomNavigationBar(
        items: _getTabBarWidget(),
        currentIndex: _currentIndex,
        showUnselectedLabels: true,
        selectedItemColor: const Color.fromARGB(255, 236, 71, 49),
        unselectedItemColor: Colors.black,
        selectedLabelStyle: TextStyle(
          fontWeight: FontWeight.bold,
          color: const Color.fromARGB(255, 236, 71, 49),
        ),
        unselectedLabelStyle: TextStyle(fontWeight: FontWeight.bold),
        onTap: (value) => {
          setState(() {
            _currentIndex = value;
          }),
        },
      ),
    );
  }
}
