\***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***andriod\***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***
andriod环境：
1、安装jdk17版本(Oracle官网下载连接: https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html，配置环境变量地址是jdk下的bin路径)

2、安装Andriod studio

> > > > 2-1、下载链接: https://developer.android.google.cn/studio?hl=zh-cn
> > > > 2-2、安装Andriod studio----环境配置（取消）----默认jdk地址不要更改
> > > > 2-3、安装插件--flutter，dart
> > > > 2-4、Setting--Language---Andriod SDk---SDK Tools--Andriod SDk Command-line Tool
> > > > 2-5、配置环境变量（flutter doctor --android-licenses）
> > > > 2-6、安装模拟器

3、设置Andriod sdk 环境变量
4、安装Dart和flutter插件
5、安装模拟器
6、检查环境---flutter doctor -v
7、修改# gradle的国内镜像地址
distributionUrl=https\://mirrors.cloud.tencent.com/gradle/gradle-9.1.0-all.zip
8、 repositories {
// 使用Maven的国内地址
maven { url = uri("https://maven.aliyun.com/repository/google") }
maven { url = uri("https://maven.aliyun.com/repository/releases") }
maven { url = uri("https://maven.aliyun.com/repository/central") }
maven { url = uri("https://maven.aliyun.com/repository/public") }
maven { url = uri("https://maven.aliyun.com/repository/gradle-plugin") }
maven { url = uri("https://maven.aliyun.com/repository/apache-snapshots") }
maven { url = uri("https://maven.aliyun.com/nexus/content/groups/public/") }
maven { url = uri("https://jitpack.io") }
google()
mavenCentral()
gradlePluginPortal()
}
flutter build apk --debug #生成调试版 apk （未签名，用于测试）
flutter build apk --release #生成发布版 apk（需要签名配置）
9、签名 android/key.properties

<!-- keytool -genkey -v -keystore $env:USERPROFILE\upload-keystore.jks `
        -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 `
        -alias upload -->

\***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***macos\***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***
下载xcode，直接运行模拟器即可

\***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***鸿蒙\***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***

1、下载鸿蒙版flutter(git clone https://gitcode.com/openharmony-tpc/flutter_flutter.git)
2、更改环境变量的flutter地址
3、下载安装DevEco studio (https://developer.huawei.com/consumer/cn/download/)
4、下载模拟器
5、环境变量：
TOOL_HOME (DevEco Studio安装地址)
C:\Program Files\Huawei\DevEco Studio

DEVECO_SDK_HOME
%TOOL_HOME%\sdk

HDC_HOME
%TOOL_HOME%\sdk\default\openharmony\toolchains

path:
%TOOL_HOME%\sdk\default\ohpm\bin
%TOOL_HOME%\sdk\default\openharmony\toolchains
%TOOL_HOME%\tools\hvigor\bin
%TOOL_HOME%\tools\node\bin

6、使用flutter doctor -v检验
7、降flutter版本--flutter clean----flutter pub get ------flluter create .
8、devceo中去打开ohos，签名----然后flutter run

### Windows HarmonyOS 插件路径

本项目在 F 盘，Pub 缓存也必须使用同一盘符的真实目录。缓存仍在 C 盘时，
Hvigor 会报 `The srcPath is not a relative path`；切换 `shared_preferences` 的 Git 地址不能解决跨盘路径问题。
项目的 `.vscode/settings.json` 已为 Dart/Flutter 扩展配置 `PUB_CACHE=F:\pub-cache`。
首次配置后重载 VS Code 窗口，在 PowerShell 中运行：

```powershell
$env:PUB_CACHE = 'F:\pub-cache'
flutter pub get
flutter run -d 127.0.0.1:5557
```

`ohos/hvigorconfig.ts` 会把原生插件路径统一为 Hvigor 要求的 `/` 相对路径。
不要手工修改 `.flutter-plugins-dependencies` 或 `.dart_tool/package_config.json`，它们由 `flutter pub get` 生成。
若移动项目到其他盘符，请同时调整 `PUB_CACHE` 和 `.vscode/settings.json`，再重新运行 `flutter pub get`。

9、兼容Android

> > > > > > 修改 java版本 ：android/app/build.gradle

    namespace = "com.example.hm_shop"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = "25.1.8937393"

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

> > > > > > > > 修改Android Gradle plugin、kotlin版本android/settings.gradle

plugins {
id "dev.flutter.flutter-plugin-loader" version "1.0.0"
id "com.android.application" version "8.3.1" apply false
id "org.jetbrains.kotlin.android" version "1.9.22" apply false

}
10、打包 flutter build hap --release/flutter build app --release
