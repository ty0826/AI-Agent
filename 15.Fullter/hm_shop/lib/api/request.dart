import 'package:dio/dio.dart';
import 'package:hm_shop/stores/tokenManmager.dart';
import 'package:hm_shop/viewmodels/api.dart';

class DioRequest {
  final _dio = Dio();
  DioRequest() {
    _dio.options
      ..baseUrl = GlobalContants.BASE_URl
      ..connectTimeout = Duration(seconds: GlobalContants.TIME_OUT)
      ..sendTimeout = Duration(seconds: GlobalContants.TIME_OUT)
      ..receiveTimeout = Duration(seconds: GlobalContants.TIME_OUT);
    _addInterceptor();
  }
  //拦截器
  void _addInterceptor() {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (requets, handler) {
          if (tokenManmager.getToken().isNotEmpty) {
            requets.headers = {
              'Authorization': "Bearer ${tokenManmager.getToken()}",
            };
          }
          handler.next(requets);
        },
        onResponse: (response, handler) {
          if (response.statusCode! >= 200 && response.statusCode! < 300) {
            handler.next(response);
            return;
          }
          handler.reject(DioException(requestOptions: response.requestOptions));
        },
        onError: (error, handler) {
          handler.reject(
            DioException(
              requestOptions: error.requestOptions,
              message: error.response?.data['msg'] ?? '数据加载失败',
            ),
          );
        },
      ),
    );
  }

  dynamic get(String url, {Map<String, dynamic>? parmas}) {
    return _handleReponse(_dio.get(url, queryParameters: parmas));
  }

  dynamic post(String url, {Map<String, dynamic>? data}) {
    return _handleReponse(_dio.post(url, data: data));
  }

  //结构返回结果
  Future<dynamic> _handleReponse(Future<Response<dynamic>> task) async {
    try {
      dynamic res = await task;
      final data = res.data as Map<String, dynamic>;
      if (data['code'] == GlobalContants.SUCCESS_CODE) {
        return data['result'] as dynamic;
      }
      // throw Exception("数据加载失败");
      throw DioException(
        requestOptions: res.requestOptions,
        message: data['msg'] ?? '数据加载失败',
      );
    } catch (e) {
      // throw Exception("数据加载失败$e");
      rethrow;
    }
  }
}

final requestApi = DioRequest();
