import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:hm_shop/api/home.dart';
import 'package:hm_shop/pages/home/components/HmMoreList.dart';
import 'package:hm_shop/stores/UserInfoController.dart';
import 'package:hm_shop/stores/tokenManmager.dart';
import 'package:hm_shop/viewmodels/home.dart';
import 'package:hm_shop/viewmodels/user.dart';

class PersonalView extends StatefulWidget {
  const PersonalView({super.key});

  @override
  State<PersonalView> createState() => _PersonalViewState();
}

class _PersonalViewState extends State<PersonalView> {
  final UserInfoController _UserInfoController = Get.find<UserInfoController>();

  Widget _buildHeader(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFFFFF2E8), Color(0xFFFDF6F1)],
        ),
      ),
      padding: const EdgeInsets.only(left: 20, right: 20, top: 80, bottom: 20),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Obx(() {
            return CircleAvatar(
              radius: 26,
              backgroundImage: _UserInfoController.user.value.avatar.isNotEmpty
                  ? NetworkImage(_UserInfoController.user.value.avatar)
                  : const AssetImage('lib/assets/goods_avatar.png'),
              backgroundColor: Colors.white,
            );
          }),
          const SizedBox(width: 12),
          Expanded(
            flex: 4,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Obx(() {
                  return GestureDetector(
                    onTap: () {
                      Navigator.pushNamed(context, '/login');
                    },
                    child: Text(
                      _UserInfoController.user.value.id.isNotEmpty
                          ? "${_UserInfoController.user.value.nickname}1111"
                          : "立即登录",
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  );
                }),
              ],
            ),
          ),
          Obx(() {
            return _UserInfoController.user.value.id.isNotEmpty
                ? Expanded(
                    flex: 1,
                    child: TextButton(
                      style: TextButton.styleFrom(
                        alignment: Alignment.center,
                        backgroundColor: Colors.grey,
                      ),
                      onPressed: () {
                        showDialog(
                          context: context,
                          builder: (context) {
                            return AlertDialog(
                              title: const Text('提示'),
                              content: const Text("确认退出登录？"),
                              actions: [
                                TextButton(
                                  onPressed: () {
                                    Navigator.pop(context);
                                  },
                                  style: TextButton.styleFrom(
                                    backgroundColor: Colors.grey,
                                  ),
                                  child: const Text(
                                    '取消',
                                    style: TextStyle(color: Colors.white),
                                  ),
                                ),
                                TextButton(
                                  onPressed: () {
                                    tokenManmager.removeToken();
                                    _UserInfoController.updateUserInfo(
                                      UserInfo.fromJSON({}),
                                    );
                                    Navigator.pushNamed(context, '/login');
                                  },
                                  style: TextButton.styleFrom(
                                    backgroundColor: Colors.redAccent,
                                  ),
                                  child: const Text(
                                    '确认',
                                    style: TextStyle(color: Colors.white),
                                  ),
                                ),
                              ],
                            );
                          },
                        );
                      },
                      child: const Text(
                        '退出',
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                  )
                : const Text('');
          }),
        ],
      ),
    );
  }

  Widget _buildVipCard() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 10),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        decoration: const BoxDecoration(
          color: Color.fromARGB(255, 239, 197, 153),
          borderRadius: BorderRadius.only(
            topLeft: Radius.circular(10),
            topRight: Radius.circular(10),
          ),
        ),
        child: Row(
          children: [
            Image.asset('lib/assets/ic_user_vip.png', height: 30, width: 30),
            const SizedBox(width: 10),
            const Expanded(
              child: Text(
                '升级美磁商城会员，尊享无享免邮',
                style: TextStyle(
                  fontSize: 14,
                  color: Color.fromRGBO(128, 44, 26, 1),
                ),
              ),
            ),
            TextButton(
              onPressed: () {},
              style: TextButton.styleFrom(
                backgroundColor: const Color.fromRGBO(126, 43, 26, 1),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 20),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(18),
                ),
              ),
              child: const Text('立即开通', style: TextStyle(fontSize: 12)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickActions() {
    Widget item(String pic, String label) {
      return Column(
        mainAxisSize: MainAxisSize.min, //主轴方向上包裹组件
        children: [
          Image.asset(pic, width: 30, height: 30, fit: BoxFit.cover),
          const SizedBox(height: 6),
          Text(label, style: const TextStyle(fontSize: 12)),
        ],
      );
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 10),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(10),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            item("lib/assets/ic_user_collect.png", '我的收藏'),
            item("lib/assets/ic_user_history.png", '我的足迹'),
            item("lib/assets/ic_user_unevaluated.png", '我的客服'),
          ],
        ),
      ),
    );
  }

  Widget _buildOrderModule() {
    Widget orderItem(String pic, String label) {
      return Column(
        mainAxisSize: MainAxisSize.min, //主轴方向上包裹组件
        children: [
          Image.asset(pic, width: 30, height: 30, fit: BoxFit.cover),
          const SizedBox(height: 6),
          Text(label, style: const TextStyle(fontSize: 12)),
        ],
      );
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 10),
      child: Card(
        shape: BeveledRectangleBorder(borderRadius: BorderRadius.circular(10)),
        elevation: 2, //阴影高度
        margin: const EdgeInsets.only(top: 20, bottom: 20),
        child: Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '我的订单',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  orderItem("lib/assets/ic_user_order.png", '全部订单'),
                  orderItem("lib/assets/ic_user_obligation.png", '待付款'),
                  orderItem("lib/assets/ic_user_unreceived.png", '待发货'),
                  orderItem("lib/assets/ic_user_unshipped.png", '待收货'),
                  orderItem("lib/assets/ic_user_unevaluated.png", '待评价'),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _registerEvent();
    _getCommendList();
  }

  List<GoodDetailItem> _recommendList = [];
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

  final ScrollController _controller = ScrollController();

  void _registerEvent() {
    _controller.addListener(() {
      if (_controller.position.pixels >=
          _controller.position.maxScrollExtent - 50) {
        _getCommendList();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      controller: _controller,
      slivers: [
        SliverToBoxAdapter(child: _buildHeader(context)),
        SliverToBoxAdapter(child: _buildVipCard()),
        SliverToBoxAdapter(child: _buildQuickActions()),
        SliverToBoxAdapter(child: _buildOrderModule()),
        //吸顶
        SliverPersistentHeader(delegate: _StickCategory(), pinned: true),
        HmmorelistView(recommendList: _recommendList),
      ],
    );
  }
}

class _StickCategory extends SliverPersistentHeaderDelegate {
  @override
  Widget build(
    BuildContext context,
    double shrinkOffset,
    bool overlapsContent,
  ) {
    return Container(
      alignment: Alignment.center,
      color: Colors.white,
      child: const Text('猜你喜欢', style: TextStyle(fontSize: 20)),
    );
  }

  @override
  // TODO: implement maxExtent
  double get maxExtent => 60;

  @override
  // TODO: implement minExtent
  double get minExtent => 60;

  @override
  bool shouldRebuild(covariant SliverPersistentHeaderDelegate oldDelegate) {
    return false;
  }
}
