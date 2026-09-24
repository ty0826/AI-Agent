import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:hm_shop/api/login.dart';
import 'package:hm_shop/stores/UserInfoController.dart';
import 'package:hm_shop/stores/tokenManmager.dart';
import 'package:hm_shop/utils/ToastUtil.dart';
import 'package:hm_shop/utils/loadingDialog.dart';
import 'package:hm_shop/viewmodels/user.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final GlobalKey<FormState> _formDom = GlobalKey<FormState>();
  bool _isChecked = false;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('登录'), centerTitle: true),
      body: Form(
        key: _formDom,
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.all(30),
          color: Colors.white,
          child: Column(
            children: [
              const Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Padding(
                    padding: EdgeInsetsGeometry.only(left: 10),
                    child: Text(
                      '账号密码登录',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.left,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              TextFormField(
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '账号不能为空';
                  }
                  if (!RegExp(r"^1[3-9]\d{9}$").hasMatch(value)) {
                    return '输入正确的手机号格式';
                  }
                  return null;
                },
                controller: _phoneController,
                decoration: InputDecoration(
                  contentPadding: const EdgeInsets.all(10),
                  hintText: '请输入账号',
                  fillColor: const Color.fromRGBO(243, 243, 243, 1),
                  filled: true,
                  border: OutlineInputBorder(
                    borderSide: BorderSide.none,
                    borderRadius: BorderRadius.circular(25),
                  ),
                ),
              ),
              const SizedBox(height: 10),
              TextFormField(
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '密码不能为空';
                  }
                  // if (!RegExp(r"^[a-zA-Z0-9_]{6,16}$").hasMatch(value)) {
                  //   return '请输入6到16位字母数字下划线的密码格式';
                  // }
                  return null;
                },
                controller: _passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  contentPadding: const EdgeInsets.all(10),
                  hintText: '请输入密码',
                  fillColor: const Color.fromRGBO(243, 243, 243, 1),
                  filled: true,
                  border: OutlineInputBorder(
                    borderSide: BorderSide.none,
                    borderRadius: BorderRadius.circular(25),
                  ),
                ),
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Checkbox(
                    value: _isChecked,
                    activeColor: Colors.black,
                    checkColor: Colors.cyanAccent,
                    //形状
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                    //边框
                    side: const BorderSide(color: Colors.grey, width: 2),
                    onChanged: (val) {
                      _isChecked = val ?? false;
                      setState(() {});
                    },
                  ),
                  const Text.rich(
                    TextSpan(
                      children: [
                        TextSpan(text: "查看并同意"),
                        TextSpan(
                          text: '《隐私条款》',
                          style: TextStyle(color: Colors.blue),
                        ),
                        TextSpan(text: '和'),
                        TextSpan(
                          text: '《用户协议》',
                          style: TextStyle(color: Colors.blue),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: () async {
                    // 登录逻辑
                    if (_formDom.currentState?.validate() ?? false) {
                      if (_isChecked) {
                        try {
                          LoadingDialog().show(context, message: '努力登录中');
                          final UserInfo res = await userLogin({
                            "account": _phoneController.text,
                            "password": _passwordController.text,
                          });
                          LoadingDialog().hide(context);
                          tokenManmager.setToken(res.token);
                          Toastutil.showToast(context, '登录成功!');
                          Navigator.pushNamed(context, '/');
                        } catch (e) {
                          LoadingDialog().hide(context);

                          Toastutil.showToast(
                            context,
                            (e as DioException).message!,
                          );
                        }
                      } else {
                        Toastutil.showToast(context, '请勾选用户协议');
                      }
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.black,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(25),
                    ),
                  ),
                  child: const Text(
                    "登录",
                    style: TextStyle(fontSize: 18, color: Colors.white),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
