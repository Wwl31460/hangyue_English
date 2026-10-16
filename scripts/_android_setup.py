# Android 构建环境搭建：解压 cmdline-tools 并安装所需 SDK 组件
# 说明：sdkmanager 是 .bat，需经 shell 调用；本脚本一次性完成，可重复执行。
import os
import pathlib
import shutil
import subprocess
import sys
import zipfile

SDK = pathlib.Path(r'C:\Users\wwl31460\.workbuddy\binaries\android-sdk')
ZIP = SDK / 'downloads' / 'cmdtools.zip'
CT_DIR = SDK / 'cmdline-tools'
LATEST = CT_DIR / 'latest'

# ---------- 1) 解压命令行工具 ----------
if LATEST.exists():
    print('[1/3] cmdline-tools 已存在，跳过解压')
else:
    tmp = SDK / '_tmp_extract'
    if tmp.exists():
        shutil.rmtree(tmp)
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(tmp)
    CT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(str(tmp / 'cmdline-tools'), str(LATEST))
    shutil.rmtree(tmp, ignore_errors=True)
    print('[1/3] 解压完成 ->', LATEST)

# ---------- 2) 准备环境变量（ANDROID_HOME + JAVA_HOME） ----------
env = os.environ.copy()
env['ANDROID_HOME'] = str(SDK)
env['ANDROID_SDK_ROOT'] = str(SDK)

java_exe = shutil.which('java')
if java_exe:
    # 注意：which('java') 常指向 Oracle 的 javapath 转发目录，不是 JDK 根，
    # 必须问 java 自己 java.home 才是真正的 JDK 路径。
    try:
        probe = subprocess.run(
            [java_exe, '-XshowSettings:properties', '-version'],
            capture_output=True, text=True,
        )
        for line in (probe.stderr or '').splitlines():
            if 'java.home' in line and '=' in line:
                env['JAVA_HOME'] = line.split('=', 1)[1].strip()
                break
    except Exception as e:
        print('探测 java.home 失败:', e)
print('[2/3] JAVA_HOME =', env.get('JAVA_HOME', '(未找到 java)'))

sdkmanager = LATEST / 'bin' / 'sdkmanager.bat'

# ---------- 3) 接受许可 + 安装组件 ----------
PKGS = [
    'platform-tools',
    'platforms;android-35',
    'build-tools;35.0.0',
]

print('[3/3] 接受 SDK 许可 ...')
proc = subprocess.run(
    [str(sdkmanager), f'--sdk_root={SDK}', '--licenses'],
    input='y\n' * 60, text=True, encoding='utf-8', errors='replace',
    capture_output=True, env=env, shell=False,
)
print((proc.stdout or '(无输出)')[-2000:])
if proc.returncode != 0:
    print('许可步骤 stderr:', proc.stderr[-1500:], file=sys.stderr)

print('[3/3] 安装组件:', ', '.join(PKGS))
proc = subprocess.run(
    [str(sdkmanager), f'--sdk_root={SDK}', '--install', *PKGS],
    input='y\n' * 60, text=True, encoding='utf-8', errors='replace',
    capture_output=True, env=env, shell=False,
)
print((proc.stdout or '(无输出)')[-4000:])
if proc.returncode != 0:
    print('安装 stderr:', proc.stderr[-2500:], file=sys.stderr)
    sys.exit(proc.returncode)

print('DONE  SDK 安装在', SDK)
for sub in ('platform-tools', 'platforms', 'build-tools'):
    p = SDK / sub
    print(' ', sub, '->', sorted(x.name for x in p.iterdir()) if p.exists() else '(缺失)')
