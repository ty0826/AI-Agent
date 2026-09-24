void main(List<String> args) {
  PayBase pay = ZFBpay();
  pay.pay();
}

class PayBase {
  void pay() {
    print("基础支付");
  }
}

class VXpay extends PayBase {
  @override
  void pay() {
    print('微信支付');
  }
}

class ZFBpay extends PayBase {
  @override
  void pay() {
    print("支付宝支付");
  }
}
