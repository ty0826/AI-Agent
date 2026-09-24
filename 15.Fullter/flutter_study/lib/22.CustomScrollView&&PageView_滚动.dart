import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(const MainPage());
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _currentindex = 0;
  final PageController _pageController = PageController();
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text(
            'CustomScrollView&&PageView自定义布局滚动',
            style: TextStyle(color: Colors.white),
          ),
          centerTitle: true,
          backgroundColor: Colors.red,
        ),
        /**
         * SliveList--->ListView
         * SliveGrig--->GridView
         * SliverAppBar-->AppBar
         * SliverPadding-->Paddig
         * SliverToBoxAdapter--->ToBoxAdapter(用于包裹普通Widget)
         * SliverPersistentHeader(黏性吸顶)
         * PageView--->整页滚动
         */
        body: CustomScrollView(
          slivers: [
            //包裹普通widget
            SliverToBoxAdapter(
              child: Stack(
                children: [
                  Container(
                    height: 200,
                    color: Colors.amberAccent,
                    child: PageView.builder(
                      controller: _pageController,
                      itemCount: 10,
                      onPageChanged: (value) => {
                        setState(() {
                          _currentindex = value;
                        }),
                      },
                      itemBuilder: (BuildContext context, int index) =>
                          Container(
                            color: Colors.blue,
                            alignment: Alignment.center,
                            height: 200,
                            child: Text(
                              '第${index + 1}个轮播',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 20,
                              ),
                            ),
                          ),
                    ),
                  ),
                  Positioned(
                    bottom: 0,
                    left: 0,
                    right: 0,
                    child: SizedBox(
                      height: 20,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: List.generate(
                          10,
                          (index) => GestureDetector(
                            onTap: () => {
                              // _pageController.jumpToPage(index),
                              _pageController.animateToPage(
                                index,
                                duration: Duration(milliseconds: 300),
                                curve: Curves.linear,
                              ),
                              setState(() {
                                _currentindex = index;
                              }),
                            },
                            child: Container(
                              width: 10,
                              height: 10,
                              margin: EdgeInsets.only(left: 10),
                              decoration: BoxDecoration(
                                color: index == _currentindex
                                    ? Colors.red
                                    : Colors.white,
                                borderRadius: BorderRadius.circular(20),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            SliverToBoxAdapter(child: SizedBox(height: 10)),
            //吸附配置
            SliverPersistentHeader(
              delegate: _StickCategory(),
              pinned: true, //固定吸顶
            ),
            SliverToBoxAdapter(child: SizedBox(height: 10)),
            SliverPadding(
              padding: EdgeInsets.all(10),
              sliver: SliverGrid.builder(
                itemCount: 20,
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  mainAxisSpacing: 10,
                  crossAxisSpacing: 10,
                  childAspectRatio: 2 / 3,
                ),
                itemBuilder: (BuildContext context, int index) => Container(
                  padding: EdgeInsets.all(10),
                  color: Colors.amber,
                  alignment: Alignment.center,
                  child: Text(
                    '第${index + 1}个',
                    style: TextStyle(color: Colors.white, fontSize: 20),
                  ),
                ),
              ),
            ),

            SliverList.separated(
              itemCount: 10,
              itemBuilder: (BuildContext context, int index) => Container(
                height: 100,
                color: Colors.red,
                width: double.infinity,
                alignment: Alignment.center,
                child: Text(
                  '第${index + 1}个数据',
                  style: TextStyle(color: Colors.white, fontSize: 20),
                ),
              ),
              separatorBuilder: (BuildContext context, int index) => Container(
                height: 20,
                width: double.infinity,
                color: Colors.amber,
              ),
            ),
          ],
        ),
      ),
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
      child: ListView.builder(
        itemCount: 100,
        scrollDirection: Axis.horizontal,
        itemBuilder: (BuildContext context, int index) => Container(
          width: 100,
          margin: EdgeInsets.symmetric(horizontal: 10),
          color: Colors.blue,
          alignment: Alignment.center,
          child: Text('分类${index + 1}', style: TextStyle(color: Colors.white)),
        ),
      ),
    );
  }

  @override
  // TODO: implement maxExtent
  double get maxExtent => 80; //最大折叠高度

  @override
  // TODO: implement minExtent
  double get minExtent => 40; //最小折叠高度

  @override
  bool shouldRebuild(covariant SliverPersistentHeaderDelegate oldDelegate) {
    // TODO: implement shouldRebuild
    return false; //不需要重建
  }
}
