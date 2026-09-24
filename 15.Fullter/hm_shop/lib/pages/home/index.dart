import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:hm_shop/api/home.dart';
import 'package:hm_shop/viewmodels/home.dart';
import 'package:hm_shop/pages/home/components/Hmslider.dart';
import 'package:hm_shop/pages/home/components/Hmcategory.dart';
import 'package:hm_shop/pages/home/components/Hmsuggestion.dart';
import 'package:hm_shop/pages/home/components/HmHot.dart';
import 'package:hm_shop/pages/home/components/HmMoreList.dart';
import 'package:hm_shop/utils/ToastUtil.dart';

class HomeView extends StatefulWidget {
  const HomeView({super.key});

  @override
  State<HomeView> createState() => _HomeViewState();
}

class _HomeViewState extends State<HomeView> {
  List<BennerItem> _bennerList = [];
  List<CategoryItem> _categoryList = [];
  HotProductItem _hotProductList = HotProductItem(
    id: '',
    title: '',
    subTypes: [],
  );
  HotProductItem _nvogueList = HotProductItem(id: '', title: '', subTypes: []);
  HotProductItem _oneShopList = HotProductItem(id: '', title: '', subTypes: []);
  List<GoodDetailItem> _recommendList = [];
  List<Widget> _getHomeChindren() {
    return [
      SliverToBoxAdapter(child: HmsliderView(bennerList: _bennerList)),
      SliverToBoxAdapter(child: SizedBox(height: 20)),
      SliverToBoxAdapter(child: HmcategoryView(categoryList: _categoryList)),
      SliverToBoxAdapter(
        child: HmsuggestionView(hotProductList: _hotProductList),
      ),
      HmhotView(hotProductList: [_nvogueList, _oneShopList]),
      HmmorelistView(recommendList: _recommendList),
    ];
  }

  double _paddingTop = 0;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _registerEvent();
    //initState--->build---->下拉刷新组件
    Future.microtask(() {
      _paddingTop = 100;
      setState(() {});
      _key.currentState?.show();
    });
  }

  final ScrollController _controller = ScrollController();

  //监听滚动到底部事件
  void _registerEvent() {
    _controller.addListener(() {
      //pixels当前滚动距离，maxScrollExtent最大的滚动距离
      if (_controller.position.pixels >=
          (_controller.position.maxScrollExtent - 50)) {
        _getCommendList();
      }
    });
  }

  bool isMore = false;
  bool isLoding = false;
  int pageCurrent = 1;
  Future<void> _getCommendList() async {
    if (isLoding || isMore) {
      return;
    }
    int limitSize = pageCurrent * 8;
    isLoding = true;
    _recommendList = await getRecommendListApi({"limit": limitSize});
    isLoding = false;
    //当返回的数据小于设定的数据，说明没有更多数据了
    if (_recommendList.length < limitSize) {
      isMore = true;
    }
    pageCurrent++;
    setState(() {});
  }

  Future<void> _getInvogueList() async {
    _nvogueList = await getInvogueListApi();
  }

  Future<void> _getOneShopList() async {
    _oneShopList = await getOneShopListApi();
  }

  Future<void> _getBennerList() async {
    _bennerList = await getBennerListApi();
  }

  Future<void> _getCategoryList() async {
    _categoryList = await getCategoryApi();
  }

  Future<void> _getHotList() async {
    _hotProductList = await getHotList();
  }

  Future<void> _refreshData() async {
    isMore = false;
    isLoding = false;
    pageCurrent = 1;
    await _getBennerList();
    await _getCategoryList();
    await _getHotList();
    await _getInvogueList();
    await _getOneShopList();
    await _getCommendList();
    //数据获取成功
    Toastutil.showToast(context, '数据获取成功');
    _paddingTop = 0;
    setState(() {});
  }

  //GlobalKey是一个方法，可以创建一个key绑定到widget部件上，可以操作widget
  final GlobalKey<RefreshIndicatorState> _key =
      GlobalKey<RefreshIndicatorState>();
  @override
  Widget build(BuildContext context) {
    //下拉刷新
    return RefreshIndicator(
      onRefresh: _refreshData,
      key: _key,
      child: AnimatedContainer(
        padding: EdgeInsets.only(top: _paddingTop),
        duration: Duration(microseconds: 300),
        child: CustomScrollView(
          controller: _controller,
          slivers: _getHomeChindren(),
        ),
      ),
    );
  }
}
