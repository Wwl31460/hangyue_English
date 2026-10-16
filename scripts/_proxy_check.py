# 检查本机是否存在系统代理（若有，Supabase 可能仍可用）
import winreg

try:
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
    )
    for name in ('ProxyEnable', 'ProxyServer', 'ProxyOverride', 'AutoConfigURL'):
        try:
            val, _ = winreg.QueryValueEx(key, name)
            print(f'{name:<16} = {val}')
        except FileNotFoundError:
            print(f'{name:<16} = (未设置)')
    winreg.CloseKey(key)
except Exception as e:
    print('读取注册表失败:', type(e).__name__, e)
