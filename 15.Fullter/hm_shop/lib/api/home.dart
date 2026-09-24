//获取轮播数据
import 'package:hm_shop/api/request.dart';
import 'package:hm_shop/viewmodels/api.dart';
import 'package:hm_shop/viewmodels/home.dart';

Future<List<BennerItem>> getBennerListApi() async {
  return (await requestApi.get(HttpContants.BANNER_LIST) as List<dynamic>)
      .map((e) => BennerItem.fromJSON(e as Map<String, dynamic>))
      .toList();
}

Future<dynamic> getCategoryApi() async {
  return (await requestApi.get(HttpContants.CATEGORY_LIST) as List<dynamic>)
      .map((e) => CategoryItem.fromJSON(e as Map<String, dynamic>))
      .toList();
}

Future<dynamic> getHotList() async {
  return HotProductItem.fromJSON(
    await requestApi.get(HttpContants.PRODUCT_LIST) as Map<String, dynamic>,
  );
}

Future<dynamic> getInvogueListApi() async {
  return HotProductItem.fromJSON(
    await requestApi.get(HttpContants.IN_VOGUE_LIST) as Map<String, dynamic>,
  );
}

Future<dynamic> getOneShopListApi() async {
  return HotProductItem.fromJSON(
    await requestApi.get(HttpContants.ONE_STOp_LIST) as Map<String, dynamic>,
  );
}

Future<dynamic> getRecommendListApi(Map<String, dynamic> params) async {
  return (await requestApi.get(HttpContants.RECOMMRED_LIST, parmas: params)
          as List)
      .map((item) {
        return GoodDetailItem.fromJSON(item as Map<String, dynamic>);
      })
      .toList();
}
