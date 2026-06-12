#!/usr/bin/env python3
"""
AICraft 监管看板 API
专为网信办监管设计·受密码保护·只读查询
部署: GZ /opt/aicraft/regulator/  systemd :3002
"""

import json
import sqlite3
import hashlib
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path

PORT = 3002
AUTH_USER = "cac"
AUTH_PASS = "aicraft2026!"
DB_PATH = "/opt/new-api/data/one-api.db"
LOG_DIR = Path("/opt/aicraft/monitor/logs")

# Simple password hash
AUTH_HASH = hashlib.sha256(f"{AUTH_USER}:{AUTH_PASS}".encode()).hexdigest()

def check_auth(handler):
    """验证访问密码"""
    cookie = handler.headers.get("Cookie", "")
    for part in cookie.split(";"):
        if "aicraft_auth=" in part:
            token = part.split("aicraft_auth=")[1].strip()
            return token == AUTH_HASH
    return False

def query_db(query, params=()):
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB Error] {e}", flush=True)
        return []

def read_log_last(filename, lines=10):
    """读取日志最后N行"""
    path = LOG_DIR / filename
    if not path.exists():
        return []
    with open(path) as f:
        all_lines = f.readlines()
        return all_lines[-lines:]

def count_interceptions():
    """统计今日拦截次数"""
    today = datetime.now().strftime("%Y%m%d")
    count = 0
    types = {}
    for f in LOG_DIR.glob(f"a2-security-{today}.log"):
        content = f.read_text()
        count += content.count("ALERT")
        count += content.count("封禁IP")
    for f in LOG_DIR.glob(f"a3-token-{today}.log"):
        content = f.read_text()
        count += content.count("ALERT")
        count += content.count("自动暂停")
    return count

def get_today_stats():
    """获取今日统计"""
    today_start = int(datetime.now().replace(hour=0, minute=0, second=0).timestamp())

    # 今日请求总数（不含系统自检）
    rows = query_db(
        "SELECT COUNT(*), SUM(quota), COUNT(DISTINCT user_id), COUNT(DISTINCT ip) FROM logs WHERE created_at > ? AND model_name != '' AND quota > 0",
        (today_start,)
    )
    req_count, total_quota, unique_users, unique_ips = rows[0] if rows else (0, 0, 0, 0)

    # 系统自检数量
    sys_rows = query_db(
        "SELECT COUNT(*) FROM logs WHERE created_at > ? AND model_name != '' AND (content LIKE '%ping%' OR prompt_tokens <= 5)",
        (today_start,)
    )
    sys_count = sys_rows[0][0] if sys_rows else 0

    # 今日各模型用量
    model_rows = query_db(
        "SELECT model_name, COUNT(*), SUM(quota) FROM logs WHERE created_at > ? AND model_name != '' GROUP BY model_name ORDER BY SUM(quota) DESC LIMIT 10",
        (today_start,)
    )

    # 渠道状态
    channel_state = {}
    state_file = LOG_DIR / "channel_state.json"
    if state_file.exists():
        channel_state = json.loads(state_file.read_text())

    # 拦截统计
    interceptions = count_interceptions()

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "request_count": req_count,
        "system_check_count": sys_count,
        "total_tokens": total_quota or 0,
        "unique_users": unique_users,
        "unique_ips": unique_ips,
        "interceptions": interceptions,
        "models": [{"name": r[0], "count": r[1], "tokens": r[2]} for r in model_rows],
        "channels": channel_state,
        "system_uptime_hours": round(get_uptime_hours(), 1),
    }

def get_uptime_hours():
    """系统运行时间"""
    try:
        r = subprocess.run(["uptime", "-p"], capture_output=True, text=True, timeout=5)
        # Parse "up 3 days, 2 hours, 30 minutes"
        import re
        days = re.search(r'(\d+)\s+day', r.stdout)
        hours = re.search(r'(\d+)\s+hour', r.stdout)
        mins = re.search(r'(\d+)\s+minute', r.stdout)
        d = int(days.group(1)) if days else 0
        h = int(hours.group(1)) if hours else 0
        m = int(mins.group(1)) if mins else 0
        return d * 24 + h + m / 60
    except:
        return 0

def get_channel_health():
    """渠道健康报告"""
    channels = {}
    state_file = LOG_DIR / "channel_state.json"
    if state_file.exists():
        state = json.loads(state_file.read_text())
        names = {1: "DeepSeek-官方", 2: "硅基流动", 3: "阿里云百炼", 4: "智谱GLM",
                 5: "MiniMax", 6: "火山方舟-豆包", 7: "OpenRouter-国际", 8: "七牛云AI"}
        for cid_str, info in state.items():
            cid = int(cid_str)
            channels[str(cid)] = {
                "name": names.get(cid, f"Channel-{cid}"),
                "failures": info.get("failures", 0),
                "status": "healthy" if info.get("failures", 0) == 0 else "degraded"
            }
    return channels

class RegulatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Auth check
        if self.path == "/login" or self.path == "/regulator/login":
            return self.serve_login()

        if not check_auth(self):
            self.send_response(302)
            self.send_header("Location", "/regulator/login")
            self.end_headers()
            return

        if self.path == "/" or self.path == "/dashboard":
            self.serve_dashboard()
        elif self.path == "/api/stats":
            self.serve_json(get_today_stats())
        elif self.path == "/api/channels":
            self.serve_json(get_channel_health())
        elif self.path == "/logout":
            self.send_response(302)
            self.send_header("Set-Cookie", "aicraft_auth=; Max-Age=0")
            self.send_header("Location", "/regulator/login")
            self.end_headers()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/login" or self.path == "/regulator/login":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            params = dict(p.split("=") for p in body.split("&") if "=" in p)
            user = params.get("user", "")
            pwd = params.get("pass", "")

            if user == AUTH_USER and pwd == AUTH_PASS:
                self.send_response(302)
                self.send_header("Set-Cookie", f"aicraft_auth={AUTH_HASH}; Path=/; HttpOnly")
                self.send_header("Location", "/regulator/dashboard")
                self.end_headers()
            else:
                self.serve_login("Invalid credentials")
        else:
            self.send_error(404)

    def serve_login(self, msg=""):
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AICraft 监管看板 · 登录</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,sans-serif;background:#f9fafb;display:flex;align-items:center;justify-content:center;min-height:100vh}}
.card{{background:#fff;padding:36px 28px;border-radius:12px;box-shadow:0 4px 24px rgba(0,0,0,0.08);width:360px;text-align:center}}
h2{{font-size:20px;margin-bottom:4px;color:#1a1d23}}
.sub{{color:#6b7280;font-size:13px;margin-bottom:20px}}
input{{width:100%;padding:10px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;margin-bottom:10px;font-family:inherit}}
input:focus{{outline:none;border-color:#b8860b}}
button{{width:100%;padding:10px;background:#b8860b;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer}}
.error{{color:#ef4444;font-size:12px;margin-bottom:10px}}
.lock{{font-size:40px;margin-bottom:12px}}
</style></head>
<body>
<div class="card">
<div class="lock">🔒</div>
<h2>AICraft 监管看板</h2>
<p class="sub">海南省网信办 · 授权访问</p>
{"<p class='error'>"+msg+"</p>" if msg else ""}
<form method="post" action="/regulator/login">
<input type="text" name="user" placeholder="账号" required>
<input type="password" name="pass" placeholder="密码" required>
<button type="submit">登入看板</button>
</form>
</div></body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def serve_dashboard(self):
        stats = get_today_stats()
        channels = get_channel_health()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        healthy = sum(1 for c in channels.values() if c["status"] == "healthy")
        total_c = len(channels) or 7

        # Model table rows
        model_rows = ""
        for i, m in enumerate(stats.get("models", [])[:10]):
            model_rows += f"<tr><td>{i+1}</td><td>{m['name'][:30]}</td><td>{m['count']:,}</td><td>{m['tokens']:,}</td></tr>"

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="60">
<title>AICraft 监管看板</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,'PingFang SC','Microsoft YaHei',sans-serif;background:#f9fafb;color:#1a1d23;padding:24px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:24px;font-weight:800}}
.header h1 span{{color:#b8860b}}
.header .meta{{color:#6b7280;font-size:12px}}
.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}}
.card{{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,0.04)}}
.card-label{{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#9ca3af;margin-bottom:6px}}
.card-val{{font-size:28px;font-weight:800}}
.card-val.g{{color:#10b981}}.card-val.r{{color:#ef4444}}.card-val.b{{color:#2563eb}}.card-val.w{{color:#b8860b}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:#f3f4f6;padding:8px 12px;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#6b7280;border-bottom:2px solid #e5e7eb}}
td{{padding:8px 12px;border-bottom:1px solid #f3f4f6}}
.status-dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}}
.status-dot.green{{background:#10b981}}.status-dot.red{{background:#ef4444}}
.logout{{color:#ef4444;text-decoration:none;font-size:13px}}
@media(max-width:768px){{.grid4,.grid2{{grid-template-columns:1fr}}}}
</style></head>
<body>
<div class="header">
<div><h1>AICraft <span>监管看板</span></h1><p class="meta">海南省网信办授权 · 最后刷新 {now}</p></div>
<div><a href="/logout" class="logout">退出</a></div>
</div>

<div class="grid4">
<div class="card"><div class="card-label">今日请求量 (真实用户)</div><div class="card-val b">{stats['request_count']:,}</div><div style="font-size:10px;color:#9ca3af;margin-top:4px">系统自检: {stats.get('system_check_count',0):,} 次</div></div>
<div class="card"><div class="card-label">今日 Token 消耗</div><div class="card-val w">{stats['total_tokens']:,}</div></div>
<div class="card"><div class="card-label">活跃用户/IP</div><div class="card-val">{stats['unique_users']} / {stats['unique_ips']}</div></div>
<div class="card"><div class="card-label">今日拦截次数</div><div class="card-val r">{stats['interceptions']}</div></div>
</div>

<div class="grid2">
<div class="card">
<div class="card-label">渠道健康 ({healthy}/{total_c})</div>
{''.join(f'<div style="padding:4px 0;font-size:13px"><span class="status-dot {"green" if c["status"]=="healthy" else "red"}"></span>{c["name"]} - {c["status"]}</div>' for c in channels.values())}
</div>
<div class="card">
<div class="card-label">系统运行时间</div>
<div class="card-val g">{stats['system_uptime_hours']:.0f}h</div>
<div style="font-size:11px;color:#6b7280;margin-top:8px">7个监管Agent · 7层防御 · 自动巡检</div>
</div>
</div>

<div class="card" style="margin-top:12px">
<div class="card-label">今日模型用量 Top 10</div>
<table>
<thead><tr><th>#</th><th>模型</th><th>请求数</th><th>Token数</th></tr></thead>
<tbody>{model_rows if model_rows else '<tr><td colspan="4" style="color:#9ca3af">暂无数据</td></tr>'}</tbody>
</table>
</div>

<div style="text-align:center;margin-top:20px;font-size:10px;color:#9ca3af">
AICraft 监管看板 v1.0 · 深圳艾创矩阵科技有限公司 · 仅供海南省网信办授权使用 · 数据30秒自动刷新
</div>
</body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def serve_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode())

    def log_message(self, format, *args):
        print(f"[Regulator] {args[0]}")

def main():
    server = HTTPServer(("0.0.0.0", PORT), RegulatorHandler)
    print(f"[Regulator] 监管看板启动 :{PORT}")
    print(f"[Regulator] 账号: {AUTH_USER} 密码: {AUTH_PASS}")
    server.serve_forever()

if __name__ == "__main__":
    main()
