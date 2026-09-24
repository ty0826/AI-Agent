import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:hm_shop/viewmodels/home.dart';

class HmhotView extends StatefulWidget {
  final List<HotProductItem> hotProductList;
  const HmhotView({super.key, required this.hotProductList});

  @override
  State<HmhotView> createState() => _HmhotViewState();
}

class _HmhotViewState extends State<HmhotView> {
  Widget _buildHeader(int index, List<GoodItem> data) {
    return Row(
      children: [
        Text(
          index == 0 ? '一站全买' : "爆款推荐",
          style: TextStyle(
            color: Color.fromARGB(255, 86, 24, 20),
            fontSize: 18,
            fontWeight: FontWeight.w700,
          ),
        ),
        SizedBox(width: 10),
        Text(
          index == 0 ? '精心优选' : "最受欢迎",
          style: TextStyle(
            color: Color.fromARGB(255, 124, 63, 58),
            fontSize: 12,
          ),
        ),
      ],
    );
  }

  List<Widget> _buildChindren(int index, List<GoodItem> data) {
    return data.map((item) {
      return Container(
        width: 80,
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(12)),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Image.network(
                item.picture,
                width: 80,
                height: 100,
                errorBuilder: (context, error, stackTrace) => Image.asset(
                  'lib/assets/home_cmd_inner.png',
                  width: 80,
                  height: 100,
                ),
              ),
            ),
            SizedBox(height: 10),
            Text(
              "￥${item.price}",
              style: TextStyle(
                fontSize: 12,
                color: Color.fromARGB(255, 86, 24, 20),
              ),
            ),
          ],
        ),
      );
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    return SliverPadding(
      padding: EdgeInsets.all(10),
      sliver: SliverGrid.builder(
        itemCount: 2,
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          mainAxisSpacing: 10,
          crossAxisSpacing: 10,
        ),
        itemBuilder: (BuildContext context, int index) {
          final subTypes = widget.hotProductList[index].subTypes;

          final items = subTypes.isNotEmpty
              ? subTypes.first.goodsItems.items!.take(2).toList()
              : <GoodItem>[];

          return Container(
            padding: EdgeInsets.all(12),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              color: index == 1
                  ? const Color.fromARGB(255, 249, 247, 219)
                  : const Color.fromARGB(255, 211, 228, 240),
            ),
            child: Column(
              children: [
                _buildHeader(index, items),
                SizedBox(height: 10),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: _buildChindren(index, items),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
