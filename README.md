# 航悦英语

K12 英语单词与听读练习应用。一套前端代码，同时跑在 **手机 / 平板（Android）**、**电脑（Windows）** 和浏览器上。

- 单词：分年级、分单元的单词表，单词卡学习、选择题测验、单元测试
- 听读：跟读训练、录音回放、打分
- 复习：错词本、困难单词本、艾宾浩斯式复习
- 激励：学习得星星，10 ⭐ = 1 积分，连续学习天数统计
- 同步：老师后台开学生账号，同一账号可在手机和电脑之间同步进度
- 更新：App 内自动检查新版本，一键下载安装

## 技术栈

React 18 + TypeScript + Vite + Tailwind CSS，用 Capacitor 打包成 Android 应用，
用 Electron 打包成 Windows 桌面应用。语音朗读走 Edge 在线合成（微软真人语音）。

## 目录结构

```
src/                  前端源码（三个端共用）
  lib/                核心逻辑：进度存储、账号与云同步、朗读、更新检查
  pages/              各个页面
electron/main.cjs     桌面端主进程
android/              Capacitor 生成的安卓工程
scripts/              词库生成、打包、验证等辅助脚本
version.json          更新清单，App 靠读它判断有没有新版本
```

## 本地开发

```bash
npm install
npm run dev            # 浏览器里开发
npm run electron:dev   # 桌面端开发模式
```

## 构建

```bash
# 前端
npm run build

# 安卓（需要 JDK 21 + Android SDK）
npx cap sync android
cd android && ./gradlew assembleRelease

# 桌面端（Windows）
npx electron-builder --win portable
```

## 发布新版本

1. 改版本号：`android/app/build.gradle` 的 `versionCode` **必须 +1**（否则手机拒绝覆盖安装），
   `versionName` 随意；同时改 `src/lib/update.ts` 里的 `APP_VERSION` / `APP_VERSION_CODE`。
2. 按上面的步骤重新构建出 APK 和桌面版。
3. 在 GitHub 上建一个 Release，标签形如 `v1.2`，把安装包传上去作为附件
   （APK 命名 `hangyue-english-1.2.apk`，桌面版命名 `hangyue-english-1.2-windows.exe`）。
4. 改仓库根目录的 `version.json`：`version`、`versionCode`、`notes`、以及两个下载链接和文件大小。
5. 提交推送。之后已装的 App 一打开就会提示有新版本，也可以在「我的 → 检查更新」手动查。

> `version.json` 是更新功能的唯一开关。没推新版本时把它保持与当前版本一致，
> App 就会显示「已是最新版本」。

## 说明

- 云同步目前在部分网络环境下不可直连，App 会在登录失败时自动检测并提示具体原因；
  不登录也可以正常使用，学习记录都保存在本机。
- 签名密钥不上传仓库，请离线妥善保管。
