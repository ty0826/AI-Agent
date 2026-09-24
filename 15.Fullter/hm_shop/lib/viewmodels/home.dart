class BennerItem {
  String id;
  String imgUrl;
  BennerItem({required this.id, required this.imgUrl});

  //factory 类工厂转化类型，从json中解析数据
  factory BennerItem.fromJSON(Map<String, dynamic> json) {
    return BennerItem(
      id: json['id'] as String,
      imgUrl: json['imgUrl'] as String,
    );
  }
}

class CategoryItem {
  String id;
  String name;
  String picture;
  List<CategoryItem>? Children;
  CategoryItem({
    required this.id,
    required this.name,
    required this.picture,
    this.Children,
  });
  factory CategoryItem.fromJSON(Map<String, dynamic> json) {
    return CategoryItem(
      id: json["id"] ?? "",
      name: json["name"] ?? "",
      picture: json["picture"] ?? "",
      Children: json['Children'] == null
          ? null
          : (json['Children'] as List)
                .map(
                  (item) => CategoryItem.fromJSON(item as Map<String, dynamic>),
                )
                .toList(),
    );
  }
}

class GoodItem {
  String id;
  String name;
  String? desc;
  String price;
  String picture;
  int orderNum;
  GoodItem({
    required this.id,
    required this.name,
    this.desc,
    required this.picture,
    required this.price,
    required this.orderNum,
  });
  factory GoodItem.fromJSON(Map<String, dynamic> json) {
    return GoodItem(
      id: json['id']?.toString() ?? "",
      name: json['name']?.toString() ?? "",
      desc: json['desc']?.toString() ?? "",
      picture: json['picture']?.toString() ?? "",
      price: json['price']?.toString() ?? "",
      orderNum: int.tryParse(json['orderNum']?.toString() ?? "0") ?? 0,
    );
  }
}

class GoodItems {
  int count;
  int pageSize;
  int pages;
  int page;
  List<GoodItem>? items;
  GoodItems({
    required this.count,
    required this.pageSize,
    required this.page,
    required this.pages,
    this.items,
  });
  factory GoodItems.fromJSON(Map<String, dynamic> json) {
    return GoodItems(
      count: int.tryParse(json['count']?.toString() ?? "0") ?? 0,
      pageSize: int.tryParse(json['pageSize']?.toString() ?? "0") ?? 0,
      page: int.tryParse(json['page']?.toString() ?? "0") ?? 0,
      pages: int.tryParse(json['pages']?.toString() ?? "0") ?? 0,
      items: (json['items'] as List? ?? [])
          .map((item) => GoodItem.fromJSON(item as Map<String, dynamic>))
          .toList(),
    );
  }
}

class SubType {
  String id;
  String title;
  GoodItems goodsItems;
  SubType({required this.id, required this.title, required this.goodsItems});
  factory SubType.fromJSON(Map<String, dynamic> json) {
    return SubType(
      id: json['id']?.toString() ?? "",
      title: json['title']?.toString() ?? "",
      goodsItems: GoodItems.fromJSON(
        json['goodsItems'] as Map<String, dynamic>,
      ),
    );
  }
}

class HotProductItem {
  String id;
  String title;
  List<SubType> subTypes;
  HotProductItem({
    required this.id,
    required this.title,
    required this.subTypes,
  });
  factory HotProductItem.fromJSON(Map<String, dynamic> json) {
    return HotProductItem(
      id: json['id']?.toString() ?? "",
      title: json['title']?.toString() ?? "",
      subTypes: (json['subTypes'] as List? ?? [])
          .map((item) => SubType.fromJSON(item as Map<String, dynamic>))
          .toList(),
    );
  }
}

class GoodDetailItem extends GoodItem {
  int payCount = 0;
  GoodDetailItem({
    required super.id,
    required super.name,
    required super.picture,
    required super.price,
    required super.orderNum,
    required this.payCount,
    super.desc,
  }) : super();
  factory GoodDetailItem.fromJSON(Map<String, dynamic> json) {
    return GoodDetailItem(
      id: json['id']?.toString() ?? "",
      name: json['name']?.toString() ?? "",
      picture: json['picture']?.toString() ?? "",
      price: json['price']?.toString() ?? "",
      orderNum: int.tryParse(json["orderNum"]?.toString() ?? "0") ?? 0,
      payCount: int.tryParse(json["payCount"]?.toString() ?? "0") ?? 0,
    );
  }
}
