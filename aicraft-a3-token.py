#!/usr/bin/env python3
"""
AICraft A3 - Token异常检测 Agent
每分钟检查: 单Token消耗速率超阈值→自动暂停+告警
部署: GZ /opt/aicraft/monitor/  Cron: * * * * *
"""

import json
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

LOG_DIR = Path("/opt/aicraft/monitor/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = LOG_DIR / "a3_token_state.json"

# 阈值
QUOTA_BURST_PER_MIN = 50000     # 单分钟消耗超5万token → 告警
QUOTA_BURST_PER_10MIN = 200000  # 10分钟消耗超20万token → 暂停
TOKEN_PRICE_RATIO = 100         # 1 quota ≈ 多少token（new-api内部比例）


def get_db_path():
    for path in ["/opt/new-api/data/one-api.db"]:
        if os.path.exists(path):
            return path
    return None


def query_token_usage(db_path, minutes=10):
    since = int((datetime.now() - timedelta(minutes=minutes)).timestamp())
    try:
        conn = sqlite3.connect(db_path)
        rows = conn.execute(
            """SELECT token_id, token_name, user_id, SUM(quota) as total_quota,
               COUNT(*) as req_count, MAX(created_at) as last_seen
               FROM logs WHERE created_at > ? AND token_id > 0
               GROUP BY token_id ORDER BY total_quota DESC""",
            (since,)
        ).fetchall()
        conn.close()
        return rows
    except:
        return []


def get_token_info(db_path, token_id):
    try:
        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT id, key, user_id, status, used_quota, remain_quota, unlimited_quota, name FROM tokens WHERE id=?",
            (token_id,)
        ).fetchone()
        conn.close()
        return row
    except:
        return None


def pause_token(db_path, token_id, reason):
    """暂停Token"""
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("UPDATE tokens SET status=0 WHERE id=?", (token_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"paused_tokens": {}, "alerts_sent": []}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def log(level, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(entry)
    with open(LOG_DIR / f"a3-token-{datetime.now().strftime('%Y%m%d')}.log", "a") as f:
        f.write(entry + "\n")


def main():
    db_path = get_db_path()
    if not db_path:
        log("WARN", "无法连接数据库")
        return

    state = load_state()

    # 检查最近10分钟的Token消耗
    rows = query_token_usage(db_path, minutes=10)
    if not rows:
        return

    for row in rows:
        token_id, token_name, user_id, total_quota, req_count, last_seen = row
        if not token_id:
            continue

        # 跳过已暂停的
        if str(token_id) in state["paused_tokens"]:
            continue

        # 每分钟平均消耗
        quota_per_min = total_quota / 10

        if quota_per_min > QUOTA_BURST_PER_MIN:
            info = get_token_info(db_path, token_id)
            token_key_hint = info[1][:20] + "..." if info and info[1] else "unknown"

            log("ALERT", f"⚠️ Token异常消耗: {token_name}(ID:{token_id}) "
                         f"10分钟消耗{total_quota}quota | {req_count}次请求 | Key:{token_key_hint}")

        # 超高阈值 → 自动暂停
        if total_quota > QUOTA_BURST_PER_10MIN:
            if pause_token(db_path, token_id, "自动检测: 异常高消耗"):
                state["paused_tokens"][str(token_id)] = {
                    "name": token_name or "unknown",
                    "reason": f"10分钟消耗{total_quota}quota(阈{QUOTA_BURST_PER_10MIN})",
                    "paused_at": datetime.now().isoformat(),
                    "req_count": req_count,
                }
                log("ALERT", f"🔴 自动暂停Token: {token_name}(ID:{token_id}) | {total_quota}quota/10min")
            else:
                log("ERROR", f"暂停Token失败: {token_name}(ID:{token_id})")

    save_state(state)

    active_pauses = len(state["paused_tokens"])
    if active_pauses > 0:
        log("INFO", f"当前暂停Token: {active_pauses}个 | {list(state['paused_tokens'].keys())}")


if __name__ == "__main__":
    main()
