import 'package:hm_shop/api/request.dart';
import 'package:hm_shop/viewmodels/api.dart';
import 'package:hm_shop/viewmodels/user.dart';

Future<UserInfo> userLogin(Map<String, dynamic> data) async {
  return UserInfo.fromJSON(
    await requestApi.post(HttpContants.LOGIN, data: data),
  );
}

Future<UserInfo> userInfoApi() async {
  return UserInfo.fromJSON(await requestApi.get(HttpContants.USER_INFo));
}
