void main(List<String> args) {
  PayBase pay = WXpay();
  pay.pay();
}

// abstract 关键词声明一个抽象类（没有实现体）
abstract class PayBase {
  void pay(); //抽象类不实现具体方法
}

// 使用implements继承抽象类
class WXpay implements PayBase {
  @override
  void pay() {
    print('微信支付');
  }
}
