import 'package:dio/dio.dart';

void main(List<String> args) {}

class DioUtils {
  final Dio request = Dio();
  DioUtils() {
    // 基础配置
    request.options.baseUrl = ''; //基础地址
    request.options.connectTimeout = Duration(seconds: 10); //连接超时
    request.options.sendTimeout = Duration(seconds: 10); //发送超时
    request.options.receiveTimeout = Duration(seconds: 10); //接收超时
    /**
     *简写
     request.options
      ..baseUrl = ''
      ..connectTimeout = Duration(seconds: 10)
      ..sendTimeout = Duration(seconds: 10)
      ..receiveTimeout = Duration(seconds: 10);
     */

    //拦截器
    _addInterceptor();
  }
  void _addInterceptor() {
    request.interceptors.add(
      InterceptorsWrapper(
        //请求拦截器
        onRequest: (context, handler) {
          // context.headers['Authorization'] = 'Bearer $_token';
          // handler.reject(error)----拦截请求  handler.next---通过请求
          handler.next(context);
        },
        //响应拦截器
        onResponse: (context, handler) {
          // handler.reject(error)----响应拦截  handler.next---响应放过
          if (context.statusCode! >= 200 && context.statusCode! < 300) {
            handler.next(context);
            return;
          }
          //抛出异常
          handler.reject(DioException(requestOptions: context.requestOptions));
        },
        onError: (context, handler) {
          handler.reject(context);
        },
      ),
    );
  }

  // GET 请求
  Future<Response<T>> get<T>(
    String url, {
    Map<String, dynamic>? params,
    Options? options,
    CancelToken? cancelToken,
  }) {
    return request.get<T>(
      url,
      queryParameters: params,
      options: options,
      cancelToken: cancelToken,
    );
  }

  //  POST 请求
  Future<Response<T>> post<T>(
    String url, {
    Map<String, dynamic>? params,
    dynamic data,
    Options? options,
    CancelToken? cancelToken,
  }) {
    return request.post<T>(
      url,
      queryParameters: params,
      data: data,
      options: options,
      cancelToken: cancelToken,
    );
  }

  // PUT 请求
  Future<Response<T>> put<T>(
    String url, {
    Map<String, dynamic>? params,
    dynamic data,
    Options? options,
    CancelToken? cancelToken,
  }) {
    return request.put<T>(
      url,
      queryParameters: params,
      data: data,
      options: options,
      cancelToken: cancelToken,
    );
  }

  /// DELETE 请求
  Future<Response<T>> delete<T>(
    String url, {
    Map<String, dynamic>? params,
    dynamic data,
    Options? options,
    CancelToken? cancelToken,
  }) {
    return request.delete<T>(
      url,
      queryParameters: params,
      data: data,
      options: options,
      cancelToken: cancelToken,
    );
  }
}
