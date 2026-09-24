import 'package:carousel_slider/carousel_slider.dart';
import 'package:flutter/material.dart';
import 'package:hm_shop/viewmodels/home.dart';

class HmsliderView extends StatefulWidget {
  final List<BennerItem> bennerList;
  const HmsliderView({super.key, required this.bennerList});

  @override
  State<HmsliderView> createState() => _HmsliderViewState();
}

class _HmsliderViewState extends State<HmsliderView> {
  int _currentIndex = 0;
  final CarouselSliderController _controller = CarouselSliderController();
  Widget _getSlider(double viewWidth) {
    // 轮播插件
    return CarouselSlider(
      carouselController: _controller,
      items: List.generate(widget.bennerList.length, (int index) {
        return Image.network(
          widget.bennerList[index].imgUrl,
          fit: BoxFit.fill,
          width: viewWidth,
        );
      }),
      options: CarouselOptions(
        autoPlayInterval: Duration(seconds: 2),
        height: 300,
        viewportFraction: 1,
        autoPlay: true,
        onPageChanged: (index, reason) => {
          _currentIndex = index,
          setState(() {}),
        },
      ),
    );
  }

  Widget _getSearch() {
    return Positioned(
      left: 0,
      top: MediaQuery.of(context).padding.top,
      right: 0,
      child: Padding(
        padding: EdgeInsets.all(10),
        child: Container(
          height: 40,
          padding: EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: const Color.fromRGBO(0, 0, 0, 0.4),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Text(
            "搜索......",
            style: TextStyle(color: Colors.white, fontSize: 16),
            textAlign: TextAlign.left,
          ),
        ),
      ),
    );
  }

  Widget _getDots() {
    return Positioned(
      left: 0,
      bottom: 0,
      right: 0,
      child: SizedBox(
        width: double.infinity,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: List.generate(
            widget.bennerList.length,
            (index) => GestureDetector(
              onTap: () => {_controller.jumpToPage(index)},
              child: AnimatedContainer(
                duration: Duration(milliseconds: 300),
                width: _currentIndex == index ? 40 : 20,
                height: 4,
                margin: EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: _currentIndex == index
                      ? Color.fromRGBO(0, 0, 0, 0.4)
                      : Colors.white,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // flutter中获取设备宽度
    final double viewWidth = MediaQuery.sizeOf(context).width;
    return Stack(children: [_getSlider(viewWidth), _getSearch(), _getDots()]);
  }
}
