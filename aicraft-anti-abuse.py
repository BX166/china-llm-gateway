#!/usr/bin/env python3
"""
AICraft - 防薅羊毛 Agent
检测: 多账号/IP池/Free档滥用/邮箱别名/批量注册
部署: GZ /opt/aicraft/monitor/ · cron每10分钟
"""

import json
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

DB_PATH = "/opt/new-api/data/one-api.db"
LOG_DIR = Path("/opt/aicraft/monitor/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
ALERT_FILE = LOG_DIR / "anti_abuse_alerts.json"

# 检测规则
FREE_TIER_LIMIT = 5_000_000       # Free档月配额
MAX_ACCOUNTS_PER_IP = 3           # 单IP最多账户数
MAX_FREE_ACCOUNTS_PER_IP = 2      # 单IP最多Free账户
MAX_REGISTER_PER_HOUR = 5         # 每小时注册上限
MAX_IP_CHANGE_PER_HOUR = 3        # 每小时IP切换次数
EMAIL_ALIAS_PATTERN = re.compile(r'[.+].*@')  # user+xxx@gmail.com

def query_db(query, params=()):
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return rows
    except:
        return []

def log(level, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(entry)
    with open(LOG_DIR / f"anti_abuse_{datetime.now().strftime('%Y%m%d')}.log", "a") as f:
        f.write(entry + "\n")

def save_alert(alert):
    alerts = []
    if ALERT_FILE.exists():
        alerts = json.loads(ALERT_FILE.read_text())
    alerts.append(alert)
    ALERT_FILE.write_text(json.dumps(alerts[-100:], indent=2))  # 保留最近100条

def detect_multi_accounts():
    """检测同IP多账户"""
    since = int((datetime.now() - timedelta(hours=24)).timestamp())
    rows = query_db(
        "SELECT ip, COUNT(DISTINCT user_id) as cnt, GROUP_CONCAT(DISTINCT user_id) "
        "FROM logs WHERE created_at > ? AND ip != '' AND user_id > 0 "
        "GROUP BY ip HAVING cnt > ?",
        (since, MAX_ACCOUNTS_PER_IP)
    )
    alerts = []
    for ip, count, users in rows:
        log("ALERT", f"同IP多账户: {ip} 关联{count}个账户")
        alerts.append({"type":"multi_account","ip":ip,"accounts":count,"users":users,"time":datetime.now().isoformat()})
    return alerts

def detect_free_abuse():
    """检测Free档滥用"""
    # 查Free档Token总消耗
    rows = query_db(
        "SELECT t.id, t.key, t.name, SUM(l.quota) as used, COUNT(DISTINCT l.ip) as ips "
        "FROM tokens t JOIN logs l ON t.id = l.token_id "
        "WHERE l.created_at > ? AND t.remain_quota > 0 "
        "GROUP BY t.id HAVING used > ?",
        (int((datetime.now() - timedelta(days=1)).timestamp()), FREE_TIER_LIMIT // 30)
    )
    WHITELIST_NAMES = {"HK-Proxy", "Test-Key", "AICraft-Monitor"}
    for tid, key, name, used, ips in rows:
        if name in WHITELIST_NAMES:
            continue  # 跳过内部监控Token
        log("ALERT", f"Free档异常: {name}(ID:{tid}) 日消耗{used}quota 关联{ips}个IP")
    return []

def detect_email_aliases():
    """检测Gmail别名批量注册"""
    rows = query_db("SELECT id, email FROM users WHERE email LIKE '%+%' AND email LIKE '%@gmail%'")
    if rows:
        users_by_domain = defaultdict(list)
        for uid, email in rows:
            base = re.sub(r'\+.*?@', '@', email)
            users_by_domain[base].append(email)
        for base, aliases in users_by_domain.items():
            if len(aliases) >= 2:
                log("ALERT", f"邮箱别名批量注册: {base} → {len(aliases)}个别名 ({aliases[:3]}...)")
    return []

def detect_rapid_ip_switching():
    """检测频繁切换IP（可能是代理池）"""
    since = int((datetime.now() - timedelta(hours=1)).timestamp())
    rows = query_db(
        "SELECT user_id, COUNT(DISTINCT ip) as ip_count FROM logs "
        "WHERE created_at > ? AND user_id > 0 GROUP BY user_id HAVING ip_count > ?",
        (since, MAX_IP_CHANGE_PER_HOUR)
    )
    for user_id, count in rows:
        log("ALERT", f"频繁IP切换: 用户{user_id} 1小时内{count}个IP")

def main():
    log("INFO", "防薅羊毛巡检开始")
    alerts = detect_multi_accounts()
    detect_free_abuse()
    detect_email_aliases()
    detect_rapid_ip_switching()
    for a in alerts:
        save_alert(a)
    log("INFO", f"完成 | 告警:{len(alerts)}")

if __name__ == "__main__":
    main()
