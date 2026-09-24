import 'package:flutter/material.dart';
import 'package:hm_shop/viewmodels/home.dart';

class HmsuggestionView extends StatefulWidget {
  final HotProductItem hotProductList;
  const HmsuggestionView({super.key, required this.hotProductList});

  @override
  State<HmsuggestionView> createState() => _HmsuggestionViewState();
}

class _HmsuggestionViewState extends State<HmsuggestionView> {
  //取前三条数据
  List<GoodItem> _getDisplayitems() {
    if (widget.hotProductList.subTypes.isEmpty) return [];
    return widget.hotProductList.subTypes.first.goodsItems.items!
        .take(3)
        .toList();
  }

  Widget _buildHeader() {
    return Row(
      children: [
        Text(
          '特惠推荐',
          style: TextStyle(
            color: Color.fromARGB(255, 86, 24, 20),
            fontSize: 18,
            fontWeight: FontWeight.w700,
          ),
        ),
        SizedBox(width: 20),
        Text(
          '精选省攻略',
          style: TextStyle(
            fontSize: 12,
            color: Color.fromARGB(255, 124, 63, 58),
          ),
        ),
      ],
    );
  }

  Widget _buildLeft() {
    return Container(
      width: 100,
      height: 160,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        image: DecorationImage(
          image: AssetImage('lib/assets/home_cmd_inner.png'),
          fit: BoxFit.cover,
        ),
      ),
    );
  }

  List<Widget> _buildRight() {
    List<GoodItem> list = _getDisplayitems();
    return List.generate(list.length, (int index) {
      return Column(
        children: [
          //包裹子集，让图片有圆角
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.network(
              list[index].picture,
              width: 80,
              height: 140,
              fit: BoxFit.cover,
            ),
          ),
          SizedBox(height: 10),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              color: Color.fromARGB(255, 240, 96, 12),
            ),
            child: Text(
              '￥${list[index].price}',
              style: TextStyle(color: Colors.white),
            ),
          ),
        ],
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(5),
      child: Container(
        padding: EdgeInsets.all(12),
        alignment: Alignment.center,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          image: DecorationImage(
            image: AssetImage('lib/assets/home_cmd_sm.png'),
            fit: BoxFit.cover,
          ),
        ),
        child: Column(
          children: [
            _buildHeader(),
            SizedBox(height: 10),
            Row(
              children: [
                _buildLeft(),
                Expanded(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: _buildRight(),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
