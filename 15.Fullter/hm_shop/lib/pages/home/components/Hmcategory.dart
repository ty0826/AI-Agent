import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:hm_shop/viewmodels/home.dart';

class HmcategoryView extends StatefulWidget {
  final List<CategoryItem> categoryList;
  const HmcategoryView({super.key, required this.categoryList});

  @override
  State<HmcategoryView> createState() => _HmcategoryViewState();
}

class _HmcategoryViewState extends State<HmcategoryView> {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 100,
      child: ListView.builder(
        itemCount: widget.categoryList.length,
        scrollDirection: Axis.horizontal,
        itemBuilder: (BuildContext context, int index) {
          CategoryItem categoryData = widget.categoryList[index];
          return Container(
            margin: EdgeInsets.symmetric(horizontal: 10),
            alignment: Alignment.center,
            width: 80,
            height: 100,
            decoration: BoxDecoration(
              color: Color.fromARGB(255, 231, 232, 234),
              borderRadius: BorderRadius.circular(40),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.network(categoryData.picture, width: 40, height: 40),
                Text(categoryData.name, style: TextStyle(color: Colors.black)),
              ],
            ),
          );
        },
      ),
    );
  }
}
