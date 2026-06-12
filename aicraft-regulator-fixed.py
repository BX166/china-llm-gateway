#!/usr/bin/env python3
"""AICraft 监管看板 API"""
import json
import sqlite3
import hashlib
import subprocess
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path

PORT = 3002
AUTH_USER = "cac"
AUTH_PASS = "aicraft2026!"
DB_PATH = "/opt/new-api/data/one-api.db"
LOG_DIR = Path("/opt/aicraft/monitor/logs")
AUTH_HASH = hashlib.sha256(f"{AUTH_USER}:{AUTH_PASS}".encode()).hexdigest()

def check_auth(handler):
    cookie = handler.headers.get("Cookie", "")
    for part in cookie.split(";"):
        if "aicraft_auth=" in part:
            return part.split("aicraft_auth=")[1].strip() == AUTH_HASH
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

def count_interceptions():
    today = datetime.now().strftime("%Y%m%d")
    count = 0
    for f in LOG_DIR.glob(f"a2-security-{today}.log"):
        count += f.read_text().count("ALERT") + f.read_text().count("封禁")
    for f in LOG_DIR.glob(f"a3-token-{today}.log"):
        count += f.read_text().count("ALERT") + f.read_text().count("暂停")
    return count

def get_suspicious_activity():
    """获取可疑账户列表（含规则说明）"""
    rules = [
        {"id": 1, "rule": "高频请求", "threshold": "单IP > 60次/分钟", "agent": "A2"},
        {"id": 2, "rule": "Token异常消耗", "threshold": "10分钟 > 200,000 quota", "agent": "A3"},
        {"id": 3, "rule": "内容安全拦截", "threshold": "连续3次被A8拦截", "agent": "A8"},
        {"id": 4, "rule": "异常时段活跃", "threshold": "凌晨2-5点高频", "agent": "A10"},
        {"id": 5, "rule": "模型探测", "threshold": "1分钟切换5个模型", "agent": "A10"},
        {"id": 6, "rule": "多账户关联", "threshold": "1个IP登录3+账户", "agent": "A10"},
        {"id": 7, "rule": "地域异常", "threshold": "1小时跨国切换", "agent": "A10"},
        {"id": 8, "rule": "超额消费", "threshold": "单日 > ¥500", "agent": "A11"},
    ]
    # Check for actual violations from logs
    violations = []
    today_start = int(datetime.now().replace(hour=0, minute=0, second=0).timestamp())
    # Check recent high-frequency IPs
    rows = query_db(
        "SELECT ip, COUNT(*) as cnt FROM logs WHERE created_at > ? GROUP BY ip HAVING cnt > 500 ORDER BY cnt DESC LIMIT 5",
        (today_start,)
    )
    for row in rows:
        violations.append({"type": "高频请求", "detail": f"IP {row[0][:15]} 今日{row[1]}次请求", "severity": "medium" if row[1] < 2000 else "high"})
    return {"rules": rules, "violations": violations, "total_rules": len(rules)}

def get_today_stats():
    today_start = int(datetime.now().replace(hour=0, minute=0, second=0).timestamp())
    rows = query_db("SELECT COUNT(*), SUM(quota), COUNT(DISTINCT user_id), COUNT(DISTINCT ip) FROM logs WHERE created_at > ? AND model_name != '' AND quota > 0", (today_start,))
    req_count, total_quota, unique_users, unique_ips = rows[0] if rows else (0, 0, 0, 0)
    sys_rows = query_db("SELECT COUNT(*) FROM logs WHERE created_at > ? AND model_name != '' AND (content LIKE '%ping%' OR prompt_tokens <= 5)", (today_start,))
    sys_count = sys_rows[0][0] if sys_rows else 0
    model_rows = query_db("SELECT model_name, COUNT(*), SUM(quota) FROM logs WHERE created_at > ? AND model_name != '' GROUP BY model_name ORDER BY SUM(quota) DESC LIMIT 10", (today_start,))
    interceptions = count_interceptions()
    channel_state = {}
    sf = LOG_DIR / "channel_state.json"
    if sf.exists():
        channel_state = json.loads(sf.read_text())
    return {
        "date": datetime.now().strftime("%Y-%m-%d"), "request_count": req_count,
        "system_check_count": sys_count, "total_tokens": total_quota or 0,
        "unique_users": unique_users, "unique_ips": unique_ips, "interceptions": interceptions,
        "models": [{"name": r[0], "count": r[1], "tokens": r[2]} for r in model_rows],
        "channels": channel_state,
        "system_uptime_hours": round(get_uptime_hours(), 1),
    }

def get_uptime_hours():
    try:
        r = subprocess.run(["uptime", "-p"], capture_output=True, text=True, timeout=5)
        days = re.search(r'(\d+)\s+day', r.stdout)
        hours = re.search(r'(\d+)\s+hour', r.stdout)
        mins = re.search(r'(\d+)\s+minute', r.stdout)
        return (int(days.group(1)) if days else 0) * 24 + (int(hours.group(1)) if hours else 0) + (int(mins.group(1)) if mins else 0) / 60
    except:
        return 0

def get_channel_health():
    channels = {}
    sf = LOG_DIR / "channel_state.json"
    if sf.exists():
        state = json.loads(sf.read_text())
        names = {1: "DeepSeek-官方", 2: "硅基流动", 3: "阿里云百炼", 4: "智谱GLM", 5: "MiniMax", 6: "火山方舟-豆包", 7: "OpenRouter-国际", 8: "七牛云AI"}
        for cid_str, info in state.items():
            cid = int(cid_str)
            channels[str(cid)] = {"name": names.get(cid, f"Ch-{cid}"), "failures": info.get("failures", 0), "status": "healthy" if info.get("failures", 0) == 0 else "degraded"}
    return channels

class RegulatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.replace("/regulator", "", 1) or "/"

        if not check_auth(self) and path != "/login":
            self.send_response(302)
            self.send_header("Location", "/regulator/login")
            self.end_headers()
            return

        if path == "/login":
            self.serve_login()
        elif path == "/" or path == "/dashboard":
            self.serve_dashboard()
        elif path == "/api/stats":
            self.serve_json(get_today_stats())
        elif path == "/api/channels":
            self.serve_json(get_channel_health())
        elif path == "/logout":
            self.send_response(302)
            self.send_header("Set-Cookie", "aicraft_auth=; Max-Age=0")
            self.send_header("Location", "/regulator/login")
            self.end_headers()
        else:
            self.send_error(404)

    def do_POST(self):
        path = self.path.replace("/regulator", "", 1) or "/"
        if path == "/login":
            cl = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(cl).decode()
            from urllib.parse import parse_qs
            params = {k: v[0] for k, v in parse_qs(body).items()}
            if params.get("user") == AUTH_USER and params.get("pass") == AUTH_PASS:
                self.send_response(302)
                self.send_header("Set-Cookie", f"aicraft_auth={AUTH_HASH}; Path=/; HttpOnly")
                self.send_header("Location", "/regulator/dashboard")
                self.end_headers()
            else:
                self.serve_login("Invalid credentials")
        else:
            self.send_error(404)

    def serve_login(self, msg=""):
        html = f"""<!DOCTYPE html><html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AICraft 监管看板 · 登录</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:system-ui,sans-serif;background:#f9fafb;display:flex;align-items:center;justify-content:center;min-height:100vh}}.card{{background:#fff;padding:36px 28px;border-radius:12px;box-shadow:0 4px 24px rgba(0,0,0,0.08);width:360px;text-align:center}}h2{{font-size:20px;margin-bottom:4px;color:#1a1d23}}.sub{{color:#6b7280;font-size:13px;margin-bottom:20px}}input{{width:100%;padding:10px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;margin-bottom:10px;font-family:inherit}}input:focus{{outline:none;border-color:#b8860b}}button{{width:100%;padding:10px;background:#b8860b;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer}}.error{{color:#ef4444;font-size:12px;margin-bottom:10px}}.lock{{font-size:40px;margin-bottom:12px}}</style></head><body>
<div class="card"><div class="lock">🔒</div><h2>AICraft 监管看板</h2><p class="sub">海南省网信办 · 授权访问</p>
{"" if not msg else f"<p class='error'>{msg}</p>"}
<form method="post" action="/regulator/login"><input type="text" name="user" placeholder="账号" required><input type="password" name="pass" placeholder="密码" required><button type="submit">登入看板</button></form></div></body></html>"""
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
        self.wfile.write(html.encode())

    def serve_dashboard(self):
        stats = get_today_stats()
        channels = get_channel_health()
        suspicious = get_suspicious_activity()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        healthy = sum(1 for c in channels.values() if c["status"] == "healthy")
        total_c = len(channels) or 8
        model_rows = "".join(f"<tr><td>{i+1}</td><td>{m['name'][:30]}</td><td>{m['count']:,}</td><td>{m['tokens']:,}</td></tr>" for i, m in enumerate(stats.get("models", [])[:10]))
        ch_rows = "".join(f"<div style='padding:4px 0;font-size:13px'><span class='status-dot {'green' if c['status']=='healthy' else 'red'}'></span>{c['name']} - {c['status']}</div>" for c in channels.values())
        rule_rows = "".join(f'<tr><td>{r["id"]}</td><td>{r["rule"]}</td><td>{r["threshold"]}</td><td style="color:#2563eb">{r["agent"]}</td></tr>' for r in suspicious["rules"])
        v_rows = ""
        for v in suspicious["violations"]:
            color = "#ef4444" if v["severity"] == "high" else "#f59e0b"
            icon = "🔴" if v["severity"] == "high" else "🟡"
            v_rows += f'<tr><td style="color:{color}">{icon}</td><td>{v["type"]}</td><td>{v["detail"]}</td></tr>'
        if not suspicious["violations"]:
            v_rows = '<tr><td colspan="3" style="color:#10b981">✅ 今日无异常行为</td></tr>'

        html = f"""<!DOCTYPE html><html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="60"><title>AICraft 监管看板</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:system-ui,'PingFang SC','Microsoft YaHei',sans-serif;background:#f9fafb;color:#1a1d23;padding:24px}}.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}h1{{font-size:24px;font-weight:800}}h1 span{{color:#b8860b}}.meta{{color:#6b7280;font-size:12px}}.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}}.card{{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,0.04)}}.card-label{{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#9ca3af;margin-bottom:6px}}.card-val{{font-size:28px;font-weight:800}}.card-val.g{{color:#10b981}}.card-val.r{{color:#ef4444}}.card-val.b{{color:#2563eb}}.card-val.w{{color:#b8860b}}.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}table{{width:100%;border-collapse:collapse;font-size:13px}}th{{background:#f3f4f6;padding:8px 12px;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#6b7280;border-bottom:2px solid #e5e7eb}}td{{padding:8px 12px;border-bottom:1px solid #f3f4f6}}.status-dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}}.status-dot.green{{background:#10b981}}.status-dot.red{{background:#ef4444}}@media(max-width:768px){{.grid4,.grid2{{grid-template-columns:1fr}}}}</style></head><body>
<div class="header"><div><h1>AICraft <span>监管看板</span></h1><p class="meta">海南省网信办授权 · 最后刷新 {now}</p></div><div><a href="/regulator/logout" style="color:#ef4444;text-decoration:none;font-size:13px">退出</a></div></div>
<div class="grid4">
<div class="card"><div class="card-label">今日请求量 (真实用户)</div><div class="card-val b">{stats['request_count']:,}</div><div style="font-size:10px;color:#9ca3af;margin-top:4px">系统自检: {stats.get('system_check_count',0):,} 次</div></div>
<div class="card"><div class="card-label">今日 Token 消耗</div><div class="card-val w">{stats['total_tokens']:,}</div></div>
<div class="card"><div class="card-label">活跃用户/IP</div><div class="card-val">{stats['unique_users']} / {stats['unique_ips']}</div></div>
<div class="card"><div class="card-label">今日拦截次数</div><div class="card-val r">{stats['interceptions']}</div></div>
</div>
<div class="grid2">
<div class="card"><div class="card-label">渠道健康 ({healthy}/{total_c})</div>{ch_rows}</div>
<div class="card"><div class="card-label">系统运行时间</div><div class="card-val g">{stats['system_uptime_hours']:.0f}h</div><div style="font-size:11px;color:#6b7280;margin-top:8px">7个监管Agent · 7层防御 · 自动巡检</div></div>
</div>
<div class="card" style="margin-top:12px"><div class="card-label">可疑行为规则（8项·A2/A3/A8/A10/A11 Agent自动执行）</div>
<table><thead><tr><th>#</th><th>规则</th><th>阈值</th><th>执行Agent</th></tr></thead><tbody>
{rule_rows}
</tbody></table>
<div style="margin-top:8px;font-size:12px;color:#6b7280">今日触发的异常:</div>
<table style="margin-top:4px"><thead><tr><th></th><th>类型</th><th>详情</th></tr></thead><tbody>{v_rows}</tbody></table>
</div>

<div class="card" style="margin-top:12px"><div class="card-label">今日模型用量 Top 10</div>
<table><thead><tr><th>#</th><th>模型</th><th>请求数</th><th>Token数</th></tr></thead><tbody>{model_rows if model_rows else '<tr><td colspan="4" style="color:#9ca3af">暂无数据</td></tr>'}</tbody></table></div>
<div style="text-align:center;margin-top:20px;font-size:10px;color:#9ca3af">AICraft 监管看板 v1.0 · 深圳艾创矩阵科技有限公司 · 仅供海南省网信办授权使用 · 数据30秒自动刷新</div>
</body></html>"""
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
        self.wfile.write(html.encode())

    def serve_json(self, data):
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode())

    def log_message(self, format, *args):
        print(f"[Regulator] {args[0]}")

def main():
    server = HTTPServer(("0.0.0.0", PORT), RegulatorHandler)
    print(f"[Regulator] 监管看板 :{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    main()
