#!/usr/bin/env python3
"""
AICraft A1 - 渠道健康监控 Agent
每分钟检查所有渠道，异常时输出告警日志
部署: 广州服务器 /opt/aicraft/monitor/
Cron: * * * * * python3 /opt/aicraft/monitor/monitor.py
"""

import json
import os
import sqlite3
import subprocess
import time
from datetime import datetime
from pathlib import Path

# 配置
NEW_API_URL = "http://localhost:3000"
DB_PATH = "/opt/new-api/data/one-api.db"  # GZ实际路径
LOG_DIR = Path("/opt/aicraft/monitor/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 渠道名称映射 (从数据库读取)
# 备用静态映射
CHANNEL_NAMES = {
    1: "DeepSeek-官方",
    2: "硅基流动",
    3: "阿里云百炼",
    4: "智谱GLM",
    5: "MiniMax",
    6: "火山方舟-豆包",
    7: "OpenRouter-国际",
    8: "七牛云AI",
}

# 每个渠道的测试模型
CHANNEL_TEST_MODELS = {
    1: "deepseek-chat",
    2: "deepseek-ai/DeepSeek-V3",
    3: "qwen-max",
    4: "glm-5",
    5: "minimax-m2.5",
    6: "ep-20260608133625-766x4",
    7: "google/gemma-3-27b-it",
    8: "qwen-turbo",
}

# 告警阈值
ALERT_AFTER_FAILURES = 2  # 连续失败 N 次后告警
STATE_FILE = LOG_DIR / "channel_state.json"


def get_channels_from_db():
    """从 new-api 数据库读取渠道列表"""
    try:
        # 尝试多个可能的数据库路径
        for db_path in [
            DB_PATH,
            "/data/one-api.db",
        ]:
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                rows = conn.execute(
                    "SELECT id, name, type, status, response_time FROM channels WHERE status=1 AND deleted_at IS NULL"
                ).fetchall()
                conn.close()
                return {r[0]: {"name": r[1].strip(), "type": r[2], "status": r[3], "response_time": r[4]} for r in rows}
    except Exception as e:
        print(f"[WARN] DB读取失败: {e}")

    # 通过 Docker exec 读取
    try:
        result = subprocess.run(
            ["docker", "exec", "new-api", "sqlite3", "/data/one-api.db",
             "SELECT id, name, type, status FROM channels WHERE status=1 AND deleted_at IS NULL;"],
            capture_output=True, text=True, timeout=10
        )
        channels = {}
        for line in result.stdout.strip().split("\n"):
            parts = line.split("|")
            if len(parts) >= 4:
                cid = int(parts[0])
                channels[cid] = {"name": parts[1].strip(), "type": int(parts[2]), "status": int(parts[3])}
        return channels
    except Exception as e:
        print(f"[WARN] Docker exec 失败: {e}")

    return {}


def test_channel(channel_id, model):
    """通过 new-api relay 测试渠道连通性"""
    start = time.time()
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-m", "20",
             f"{NEW_API_URL}/v1/chat/completions",
             "-H", "Content-Type: application/json",
             "-H", f"Authorization: Bearer {os.environ.get('AICRAFT_ADMIN_KEY', 'sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182')}",
             "-d", json.dumps({"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 1})],
            capture_output=True, text=True, timeout=25
        )
        http_code = result.stdout.strip()
        latency = int((time.time() - start) * 1000)
        return http_code == "200", http_code, latency
    except Exception as e:
        latency = int((time.time() - start) * 1000)
        return False, str(e), latency


def load_state():
    """加载状态文件"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    """保存状态文件"""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def log(level, msg):
    """写日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = LOG_DIR / f"monitor-{datetime.now().strftime('%Y%m%d')}.log"
    entry = f"[{timestamp}] [{level}] {msg}"
    print(entry)
    with open(log_file, "a") as f:
        f.write(entry + "\n")


def main():
    log("INFO", "A1 健康检查开始")

    # 获取渠道列表
    channels = get_channels_from_db()
    if not channels:
        log("WARN", "无法读取渠道列表，使用静态配置")
        channels = {cid: {"name": name, "type": 1, "status": 1} for cid, name in CHANNEL_NAMES.items()}

    state = load_state()

    for cid, info in channels.items():
        name = info["name"]
        model = CHANNEL_TEST_MODELS.get(cid, "deepseek-chat")
        ok, code, latency = test_channel(cid, model)

        # 更新状态追踪
        key = str(cid)
        if key not in state:
            state[key] = {"failures": 0, "last_ok": None, "last_fail": None}

        if ok:
            state[key]["failures"] = 0
            state[key]["last_ok"] = datetime.now().isoformat()
            log("OK", f"[{name}] ✅ HTTP {code} | {latency}ms | model={model}")
        else:
            state[key]["failures"] += 1
            state[key]["last_fail"] = datetime.now().isoformat()
            fail_count = state[key]["failures"]

            if fail_count >= ALERT_AFTER_FAILURES:
                log("ALERT", f"[{name}] 🔴 连续失败 {fail_count} 次! HTTP {code} | {latency}ms | model={model}")
            else:
                log("WARN", f"[{name}] ⚠️ 失败 #{fail_count} | HTTP {code} | {latency}ms | model={model}")

    save_state(state)

    # 输出汇总
    total = len(channels)
    failed = sum(1 for k, v in state.items() if v["failures"] > 0)
    log("INFO", f"检查完成: {total - failed}/{total} 正常" + (" 🔴" if failed > 0 else " ✅"))


if __name__ == "__main__":
    main()
