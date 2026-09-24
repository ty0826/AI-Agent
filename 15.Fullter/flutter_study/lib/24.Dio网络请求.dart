import 'package:dio/dio.dart';

void main(List<String> args) {
  Dio()
      .get('https://geek.itheima.net/v1_0/channels')
      .then((res) {
        print(res);
      })
      .catchError((error) {
        print(error);
      });
}
