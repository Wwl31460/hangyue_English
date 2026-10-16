# 解压 OpenJDK 21（Capacitor 8 要求 Java 21，本机原有的是 JDK 20）
import pathlib
import zipfile

SRC = pathlib.Path(r'C:\Users\wwl31460\.workbuddy\binaries\jdk-dl\openjdk21.zip')
DST = pathlib.Path(r'C:\Users\wwl31460\.workbuddy\binaries\jdk-21')

if DST.exists() and any(DST.rglob('bin/java.exe')):
    print('已解压过，跳过')
else:
    DST.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(SRC) as z:
        z.extractall(DST)
    print('解压完成 ->', DST)

found = list(DST.rglob('bin/java.exe'))
if not found:
    raise SystemExit('未找到 java.exe，解压可能失败')
java_home = found[0].parent.parent
print('JAVA_HOME =', java_home)

# 顺带确认版本
import subprocess
out = subprocess.run([str(found[0]), '-version'], capture_output=True, text=True)
print((out.stderr or out.stdout).strip())
