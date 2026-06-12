#!/usr/bin/env python3
"""AICraft A10 - 用户画像+行为检测 Agent · :3014"""

import json, sqlite3, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

PORT = 3014
DB_PATH = "/opt/new-api/data/one-api.db"
LOG_DIR = Path("/opt/aicraft/regulator/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
PROFILE_DIR = Path("/opt/aicraft/regulator/profiles")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

# 异常阈值
ANOMALY_RULES = {
    "burst_ratio": 3.0,        # 用量突增至平均值3倍
    "hour_spread": 18,          # 24小时中活跃超18小时=可疑
    "model_switches": 5,        # 1分钟内切换5个模型=探测
    "ip_changes": 3,            # 1小时内切换3个IP
    "cost_spike": 100,          # 单日消耗突增100元
}


def query_db(query, params=()):
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return rows
    except Exception:
        return []


def build_profile(user_id):
    """构建用户行为画像"""
    now = int(datetime.now().timestamp())
    last_24h = now - 86400
    last_1h = now - 3600

    # 24小时基础统计
    total = query_db(
        "SELECT COUNT(*), SUM(quota), COUNT(DISTINCT ip), MAX(created_at) "
        "FROM logs WHERE user_id=? AND created_at>?",
        (user_id, last_24h)
    )
    req_count, total_quota, unique_ips, last_seen = total[0] if total else (0, 0, 0, 0)

    if req_count == 0:
        return {"user_id": user_id, "status": "inactive", "requests_24h": 0}

    # 最近1小时行为
    recent = query_db(
        "SELECT model_name, created_at, ip FROM logs WHERE user_id=? AND created_at>? ORDER BY created_at DESC LIMIT 100",
        (user_id, last_1h)
    )

    # 模型切换频率
    model_seq = []
    ip_seq = []
    for r in recent:
        model_seq.append(r[0])
        ip_seq.append(r[2])
    switches = sum(1 for i in range(1, len(model_seq)) if model_seq[i] != model_seq[i - 1])

    # 时段分布
    hours_active = len(set(datetime.fromtimestamp(r[1]).hour for r in recent if r[1]))

    # 平均用量
    avg_per_hour = req_count / 24 if req_count > 0 else 0
    recent_1h_count = len(recent)

    # 异常判定
    alerts = []
    if recent_1h_count > avg_per_hour * ANOMALY_RULES["burst_ratio"]:
        alerts.append({"type": "burst", "detail": f"1h:{recent_1h_count} vs avg:{avg_per_hour:.0f}/h"})
    if hours_active >= ANOMALY_RULES["hour_spread"]:
        alerts.append({"type": "agent_like", "detail": f"active {hours_active}h/24h"})
    if switches >= ANOMALY_RULES["model_switches"]:
        alerts.append({"type": "model_probe", "detail": f"{switches} switches in recent"})
    if unique_ips >= ANOMALY_RULES["ip_changes"]:
        alerts.append({"type": "ip_hopping", "detail": f"{unique_ips} IPs in 24h"})

    return {
        "user_id": user_id,
        "status": "active",
        "requests_24h": req_count,
        "total_quota_24h": total_quota or 0,
        "unique_ips_24h": unique_ips or 0,
        "hours_active": hours_active,
        "model_switches_1h": switches,
        "alerts": alerts,
        "last_seen": datetime.fromtimestamp(last_seen).isoformat() if last_seen else None,
    }


class A10Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "agent": "A10", "rules": len(ANOMALY_RULES)}, 200)
        elif self.path.startswith("/profile/"):
            uid = self.path.split("/")[-1]
            profile = build_profile(uid)
            self.send_json(profile, 200)
        elif self.path == "/alerts":
            # 扫描最近活跃用户并报告异常
            since = int((datetime.now() - timedelta(hours=1)).timestamp())
            users = query_db(
                "SELECT DISTINCT user_id FROM logs WHERE created_at>? AND user_id>0",
                (since,)
            )
            all_alerts = []
            for (uid,) in users:
                p = build_profile(uid)
                if p.get("alerts"):
                    all_alerts.append({"user_id": uid, "alerts": p["alerts"]})
            self.send_json({"alerts": all_alerts, "checked": len(users)}, 200)
        else:
            self.send_json({"agent": "A10", "endpoints": ["/health", "/profile/{id}", "/alerts"]}, 200)

    def send_json(self, data, code=200):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args): pass


def main():
    print(f"[A10] User Profiler :{PORT} | rules: {len(ANOMALY_RULES)}")
    HTTPServer(("0.0.0.0", PORT), A10Handler).serve_forever()


if __name__ == "__main__":
    main()
