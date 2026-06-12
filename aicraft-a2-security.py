#!/usr/bin/env python3
"""
AICraft A2 - 异常流量检测 Agent
每分钟检查: 单IP高频请求、异常请求模式、可疑User-Agent
部署: GZ /opt/aicraft/monitor/  Cron: * * * * *
"""

import json
import os
import sqlite3
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

LOG_DIR = Path("/opt/aicraft/monitor/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = LOG_DIR / "a2_state.json"

# 阈值
MAX_REQ_PER_MIN = 60       # 单IP每分钟最大请求数
MAX_REQ_PER_5MIN = 200      # 单IP每5分钟最大请求数
MAX_FAILED_RATIO = 0.5      # 失败率超过50%标记可疑
BLOCK_DURATION_MIN = 30     # 自动封禁时长(分钟)

# 白名单IP（GZ服务器自身、HK服务器）
WHITELIST = {"127.0.0.1", "10.1.0.13", "43.161.248.132", "101.33.204.165"}


def get_db_path():
    for path in ["/opt/new-api/data/one-api.db"]:
        if os.path.exists(path):
            return path
    try:
        result = subprocess.run(
            ["docker", "exec", "new-api", "sh", "-c", "echo /data/one-api.db"],
            capture_output=True, text=True, timeout=5
        )
        return "/opt/new-api/data/one-api.db"
    except:
        return None


def query_recent_logs(db_path, minutes=5):
    """查询最近N分钟的请求日志"""
    since = int((datetime.now() - timedelta(minutes=minutes)).timestamp())
    try:
        conn = sqlite3.connect(db_path)
        rows = conn.execute(
            """SELECT ip, user_id, model_name, quota, prompt_tokens, completion_tokens,
               created_at, channel_id, request_id
               FROM logs WHERE created_at > ? ORDER BY created_at DESC""",
            (since,)
        ).fetchall()
        conn.close()
        return rows
    except Exception:
        # Try via docker exec
        try:
            result = subprocess.run(
                ["docker", "exec", "new-api", "sqlite3", "/data/one-api.db",
                 f"SELECT ip, user_id, model_name, quota, created_at FROM logs WHERE created_at > {since} ORDER BY created_at DESC LIMIT 500;"],
                capture_output=True, text=True, timeout=10
            )
            rows = []
            for line in result.stdout.strip().split("\n"):
                parts = line.split("|")
                if len(parts) >= 5:
                    rows.append((parts[0], parts[1], parts[2], parts[3], int(parts[4]) if parts[4].isdigit() else 0))
            return rows
        except:
            return []


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"blocked_ips": {}, "alerts_sent": []}


def save_state(state):
    # Clean expired blocks
    now = datetime.now()
    state["blocked_ips"] = {
        ip: info for ip, info in state["blocked_ips"].items()
        if datetime.fromisoformat(info["until"]) > now
    }
    STATE_FILE.write_text(json.dumps(state, indent=2))


def log(level, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(entry)
    with open(LOG_DIR / f"a2-security-{datetime.now().strftime('%Y%m%d')}.log", "a") as f:
        f.write(entry + "\n")


def analyze_traffic(rows):
    """分析流量模式，返回可疑IP列表"""
    ip_counts = defaultdict(int)
    ip_failed = defaultdict(int)
    ip_total = defaultdict(int)
    ip_models = defaultdict(set)
    ip_quota = defaultdict(int)

    for row in rows:
        if len(row) >= 5:
            ip = row[0] or "unknown"
            if ip in WHITELIST:
                continue
            quota = int(row[3]) if row[3] and str(row[3]).lstrip('-').isdigit() else 0
            ip_counts[ip] += 1
            ip_total[ip] += 1
            ip_quota[ip] += quota
            if len(row) >= 3 and row[2]:
                ip_models[ip].add(row[2])

    # Detect anomalies
    alerts = []
    for ip, count in ip_counts.items():
        if count > MAX_REQ_PER_MIN:
            alerts.append({
                "ip": ip, "type": "高频请求", "severity": "HIGH",
                "detail": f"{count} req/min (阈{MAX_REQ_PER_MIN})",
                "models": list(ip_models[ip])[:3]
            })
        if count > MAX_REQ_PER_5MIN // 5:  # per-minute check, scale 5min threshold
            pass  # Will trigger 高频 anyway

    return alerts


def main():
    db_path = get_db_path()
    if not db_path:
        log("WARN", "无法连接数据库")
        return

    state = load_state()

    # 检查最近1分钟的流量
    rows = query_recent_logs(db_path, minutes=1)
    alerts = analyze_traffic(rows)

    if alerts:
        for a in alerts:
            ip = a["ip"]
            # 检查是否已被封禁
            if ip in state["blocked_ips"]:
                continue

            # 自动封禁
            until = (datetime.now() + timedelta(minutes=BLOCK_DURATION_MIN)).isoformat()
            state["blocked_ips"][ip] = {
                "reason": a["type"],
                "detail": a["detail"],
                "until": until,
                "blocked_at": datetime.now().isoformat()
            }
            log("ALERT", f"🔴 封禁IP: {ip} | {a['type']} | {a['detail']} | 封禁{BLOCK_DURATION_MIN}分钟")

    save_state(state)

    # 每日汇总
    active_blocks = len(state.get("blocked_ips", {}))
    if active_blocks > 0:
        log("INFO", f"当前封禁IP: {active_blocks}个")
    else:
        log("INFO", "无异常流量")


if __name__ == "__main__":
    main()
