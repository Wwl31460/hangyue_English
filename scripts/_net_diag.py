# 网络可达性诊断：确认 App 各外部依赖在国内网络下的连通情况
import socket, ssl

TARGETS = [
    ('朗读/Edge-TTS', 'speech.platform.bing.com', 443),
    ('Supabase-项目', 'cqasnjbpglubtgwgkjvq.supabase.co', 443),
    ('Supabase-主站', 'supabase.com', 443),
    ('npm-官方源', 'registry.npmjs.org', 443),
    ('npm-阿里镜像', 'registry.npmmirror.com', 443),
    ('Google-下载', 'dl.google.com', 443),
    ('Maven-阿里', 'maven.aliyun.com', 443),
]

for label, host, port in TARGETS:
    try:
        infos = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
        ips = sorted({i[4][0] for i in infos})
    except Exception as e:
        print(f'{label:<16} {host:<38} DNS失败 {type(e).__name__}')
        continue

    ok = None
    for ip in ips:
        s = socket.socket()
        s.settimeout(8)
        try:
            s.connect((ip, port))
            try:
                ctx = ssl.create_default_context()
                w = ctx.wrap_socket(s, server_hostname=host)
                ok = f'TLS通 {w.version()}'
                w.close()
                break
            except Exception as e:
                ok = f'TLS阻断 {type(e).__name__}'
        except Exception as e:
            ok = f'TCP失败 {type(e).__name__}'
        finally:
            try:
                s.close()
            except Exception:
                pass

    print(f'{label:<16} {host:<38} {ok}')
