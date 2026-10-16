package com.hangyue.english;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    // 跟读录音要用麦克风。WebView 里调 getUserMedia 之前，必须先把系统的录音权限拿到，
    // 否则页面上会直接报「无法访问麦克风」。
    private static final int REQ_RECORD_AUDIO = 1001;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        // 应用内更新用的原生能力（下载安装包 + 拉起安装界面）。
        // 必须写在 super.onCreate 之前，Bridge 初始化时才会把它注册进去。
        registerPlugin(UpdaterPlugin.class);

        super.onCreate(savedInstanceState);

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(
                    this,
                    new String[]{ Manifest.permission.RECORD_AUDIO },
                    REQ_RECORD_AUDIO);
        }
    }
}
