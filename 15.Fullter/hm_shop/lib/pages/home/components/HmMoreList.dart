import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:hm_shop/viewmodels/home.dart';

class HmmorelistView extends StatefulWidget {
  final List<GoodDetailItem> recommendList;
  const HmmorelistView({super.key, required this.recommendList});

  @override
  State<HmmorelistView> createState() => _HmmorelistViewState();
}

class _HmmorelistViewState extends State<HmmorelistView> {
  Widget _getChildren(GoodDetailItem data) {
    return Container(
      color: const Color.fromRGBO(161, 226, 212, 1),
      child: Column(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: AspectRatio(
              aspectRatio: 1, //宽高比
              child: Image.network(data.picture, fit: BoxFit.cover),
            ),
          ),
          SizedBox(height: 6),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 10),
            child: Text(
              data.name,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(color: Colors.black, fontSize: 15),
            ),
          ),
          SizedBox(height: 6),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 10),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text.rich(
                  TextSpan(
                    text: "￥${data.price}",
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                    ),
                    children: [
                      TextSpan(text: '  '),
                      TextSpan(
                        text: data.price,
                        style: TextStyle(
                          decoration: TextDecoration.lineThrough,
                          color: Colors.grey,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
                Text(
                  "${data.payCount}人付款",
                  style: TextStyle(color: Colors.grey),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SliverPadding(
      padding: EdgeInsets.all(10),
      sliver: SliverGrid.builder(
        itemCount: widget.recommendList.length,
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          mainAxisSpacing: 10,
          crossAxisSpacing: 10,
          childAspectRatio: 0.76,
        ),
        itemBuilder: (BuildContext context, int index) {
          final data = widget.recommendList[index];
          return Padding(
            padding: EdgeInsets.symmetric(horizontal: 10),
            child: _getChildren(data),
          );
        },
      ),
    );
  }
}
