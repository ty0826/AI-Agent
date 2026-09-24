void main(List<String> args) {
  int score = 80;
  switch (score) {
    case 100:
      print("满分");
      break;
    case 90:
      print("优秀");
      break;
    case 80:
      print("良好");
      break;
    case 70:
      print("中等");
      break;
    case 60:
      print("及格");
      break;
    default:
      print("不及格");
  }
}
