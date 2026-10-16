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
release/web/          发布到国内站点的下载页 + 更新清单 + 安装包
version.json          更新清单的静态副本（给人看的；App 实际读云端接口，见「后端与账号」）
```

## 后端与账号

后端使用托管云服务（WorkBuddy Cloud Service），域名 `hangyue-english.app.workbuddy.host`，
国内网络可直连——**不再依赖 Supabase**（原服务器在国内被阻断，导致登录一直失败）。

云服务自带的登录方式不支持「用户名 + 密码」，因此账号表由我们自己的服务端函数管理，
App 只通过 `cloud.database.rpc(...)` 调用它们：

| 函数 | 作用 |
|---|---|
| `hy_login(用户名, 密码)` | 校验密码，返回一张 180 天有效的票据 token |
| `hy_restore(token)` | 重开 App 时核对登录态 |
| `hy_logout(token)` | 登出并作废票据 |
| `hy_create_student(口令, 用户名, 密码)` | 老师后台建号；同名即改密码（找回密码用） |
| `hy_load_progress(token)` / `hy_save_progress(token, 数据)` | 学习进度读写 |
| `hy_latest_release()` | 下发最新版本清单（更新检查用） |

数据库里 `accounts` / `progress` / `hy_sessions` / `hy_release` 四张表都开了 RLS 且
**没有任何策略、不给 anon 授权**，只能通过上面这些 `SECURITY DEFINER` 函数访问；
密码用随机盐 + SHA-256 存储，客户端只保存票据，不保存密码。

更新检查必须走云端接口而不是静态文件：静态站不返回跨域响应头，App 里 `fetch` 会被浏览器拦掉。

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
3. 把新 APK 放进 `release/web/`（命名 `hangyue-english-<版本>.apk`），
   同步更新 `release/web/version.json` 与根目录 `version.json`，
   再把 `release/web/` 重新发布一次（`workbuddy_sites_deploy`，`directory` 指向该目录）。
4. 在云数据库里更新更新清单（App 真正读的是它）：
   ```sql
   UPDATE hy_release SET payload = '<新的清单 JSON>'::jsonb, updated_at = now() WHERE id = 'latest';
   ```
5. 推送仓库。之后已装的 App 一打开就会提示有新版本，也可以在「我的 → 检查更新」手动查。

> 发版时 `hy_release.payload.versionCode` 和 `src/lib/update.ts` 的 `APP_VERSION_CODE`
> 要保持一致；没推新版本时让两者等于当前版本，App 就会显示「已是最新版本」。

## 说明

- 后端在国内可直连，登录、同步、检查更新都不需要代理。
- 不登录也可以正常使用，学习记录都保存在本机；登录后本机进度会自动传上去，
  换设备登录同一账号即可续学。
- 签名密钥不上传仓库，请离线妥善保管。
