package com.hangyue.english;

import android.app.DownloadManager;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Environment;
import android.util.Log;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/**
 * Updater —— 应用内更新用的最小原生能力，只做两件事：
 * 1) 把安装包交给系统下载器下载（通知栏自带进度，比在 WebView 里自己下更稳、更省电）；
 * 2) 下载完成后拉起系统的安装界面。
 * 页面侧的调用见 src/lib/update.ts。
 */
@CapacitorPlugin(name = "Updater")
public class UpdaterPlugin extends Plugin {

    private static final String TAG = "UpdaterPlugin";

    /** 交给系统下载器下载安装包，返回下载任务 id（后续用它查进度、取文件） */
    @PluginMethod
    public void download(PluginCall call) {
        String url = call.getString("url");
        String fileName = call.getString("fileName", "hangyue-update.apk");
        if (url == null || url.isEmpty()) {
            call.reject("缺少下载地址");
            return;
        }
        try {
            DownloadManager dm = (DownloadManager) getContext().getSystemService(Context.DOWNLOAD_SERVICE);
            if (dm == null) {
                call.reject("系统下载器不可用");
                return;
            }

            DownloadManager.Request req = new DownloadManager.Request(Uri.parse(url));
            req.setTitle("航悦英语 更新包");
            req.setDescription("正在下载 " + fileName);
            req.setMimeType("application/vnd.android.package-archive");
            req.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            // 存到公共「下载」目录：用户能在文件管理里找到，也方便出问题时手动安装
            req.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, fileName);

            long id = dm.enqueue(req);
            JSObject ret = new JSObject();
            ret.put("id", id);
            call.resolve(ret);
        } catch (Exception e) {
            Log.w(TAG, "download failed", e);
            call.reject("下载启动失败：" + e.getMessage());
        }
    }

    /** 查询下载状态：status 为 downloading / done / failed，received、total 是字节数 */
    @PluginMethod
    public void progress(PluginCall call) {
        long id = call.getLong("id", -1L);
        JSObject ret = new JSObject();
        if (id < 0) {
            ret.put("status", "failed");
            call.resolve(ret);
            return;
        }
        Cursor c = null;
        try {
            DownloadManager dm = (DownloadManager) getContext().getSystemService(Context.DOWNLOAD_SERVICE);
            c = dm.query(new DownloadManager.Query().setFilterById(id));
            if (c != null && c.moveToFirst()) {
                int status = c.getInt(c.getColumnIndexOrThrow(DownloadManager.COLUMN_STATUS));
                String s = "downloading";
                if (status == DownloadManager.STATUS_SUCCESSFUL) s = "done";
                else if (status == DownloadManager.STATUS_FAILED) s = "failed";
                ret.put("status", s);
                ret.put("received", c.getLong(c.getColumnIndexOrThrow(DownloadManager.COLUMN_BYTES_DOWNLOADED_SO_FAR)));
                ret.put("total", c.getLong(c.getColumnIndexOrThrow(DownloadManager.COLUMN_TOTAL_SIZE_BYTES)));
            } else {
                ret.put("status", "failed");
            }
        } catch (Exception e) {
            ret.put("status", "failed");
        } finally {
            if (c != null) c.close();
        }
        call.resolve(ret);
    }

    /** 下载完成后拉起系统安装界面（用户还需要自己点一下「安装」） */
    @PluginMethod
    public void install(PluginCall call) {
        long id = call.getLong("id", -1L);
        try {
            DownloadManager dm = (DownloadManager) getContext().getSystemService(Context.DOWNLOAD_SERVICE);
            Uri uri = id >= 0 ? dm.getUriForDownloadedFile(id) : null;
            if (uri == null) {
                call.reject("安装包还没准备好");
                return;
            }
            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setDataAndType(uri, "application/vnd.android.package-archive");
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
            getContext().startActivity(intent);
            call.resolve();
        } catch (Exception e) {
            Log.w(TAG, "install failed", e);
            call.reject("拉起安装界面失败：" + e.getMessage());
        }
    }

    /** 用系统浏览器打开链接（App 内下载失败时的降级方案） */
    @PluginMethod
    public void openUrl(PluginCall call) {
        String url = call.getString("url");
        if (url == null || url.isEmpty()) {
            call.reject("缺少链接");
            return;
        }
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getContext().startActivity(intent);
            call.resolve();
        } catch (Exception e) {
            call.reject("打开链接失败：" + e.getMessage());
        }
    }
}
