# 向已装好的 Android SDK 追加组件（用法：python _sdk_add.py platform-tools platforms;android-36 ...）
import os
import pathlib
import subprocess
import sys

SDK = pathlib.Path(r'C:\Users\wwl31460\.workbuddy\binaries\android-sdk')
sdkmanager = SDK / 'cmdline-tools' / 'latest' / 'bin' / 'sdkmanager.bat'

env = os.environ.copy()
env['ANDROID_HOME'] = str(SDK)
env['ANDROID_SDK_ROOT'] = str(SDK)
env['JAVA_HOME'] = r'C:\Program Files\Java\jdk-20'

pkgs = sys.argv[1:]
if not pkgs:
    print('未指定组件')
    sys.exit(1)

print('安装:', ', '.join(pkgs))
proc = subprocess.run(
    [str(sdkmanager), f'--sdk_root={SDK}', '--install', *pkgs],
    input='y\n' * 60, text=True, encoding='utf-8', errors='replace',
    capture_output=True, env=env, shell=False,
)
print((proc.stdout or '')[-3000:])
if proc.returncode != 0:
    print('stderr:', (proc.stderr or '')[-2000:], file=sys.stderr)
    sys.exit(proc.returncode)

print('DONE')
for sub in ('platforms', 'build-tools'):
    p = SDK / sub
    print(' ', sub, '->', sorted(x.name for x in p.iterdir()) if p.exists() else '(缺失)')
