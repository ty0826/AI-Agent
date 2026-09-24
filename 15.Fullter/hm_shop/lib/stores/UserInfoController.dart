import 'package:get/get.dart';
import 'package:hm_shop/viewmodels/user.dart';

class UserInfoController extends GetxController {
  var user = UserInfo.fromJSON({}).obs; //监听
  void updateUserInfo(UserInfo newUser) {
    user.value = newUser;
  }
}
/***
 * 必须先put一次，才能find，可以find多次，put仅一次就行，find是使用，put是注册
 * 通常可以直接在main.dart中注册就行
 * 
 * _UserInfoController = Get.find()---->_UserInfoController.updateUserInfo()
 * _UserInfoController = Get.put(UserInfoController())---->Obx((){
 *  retrun <Wiget>  _UserInfoController.user.vaule.....
 * 
 * })
 */