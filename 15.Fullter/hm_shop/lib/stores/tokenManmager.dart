import 'package:hm_shop/viewmodels/api.dart';
import 'package:shared_preferences/shared_preferences.dart';

class TokenManmager {
  Future<SharedPreferences> _getInstance() {
    return SharedPreferences.getInstance();
  }

  String _token = ''; //同步获取token
  Future<void> init() async {
    final prefs = await _getInstance();
    _token = prefs.getString(GlobalContants.TOKEN_KEY) ?? "";
  }

  Future<void> setToken(String value) async {
    final prefs = await _getInstance(); //获取持久化实例
    prefs.setString(GlobalContants.TOKEN_KEY, value); //将token写入持久化
    _token = value;
  }

  String getToken() {
    return _token;
  }

  void removeToken() async {
    final prefs = await _getInstance();
    prefs.remove(GlobalContants.TOKEN_KEY);
    _token = '';
  }
}

final tokenManmager = TokenManmager();
