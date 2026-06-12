#!/usr/bin/env python3
"""AICraft A12 - 审计日志 Agent · 端口3012"""

import json
import hashlib
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
from pathlib import Path

PORT = 3012
LOG_DIR = Path("/opt/aicraft/regulator/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
CHAIN_FILE = LOG_DIR / "audit_chain.json"
DB_PATH = "/opt/new-api/data/one-api.db"

def hash_entry(prev_hash, data):
    """链式哈希——每一条记录链接前一条，不可篡改"""
    payload = prev_hash + json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()

def get_prev_hash():
    if CHAIN_FILE.exists():
        chain = json.loads(CHAIN_FILE.read_text())
        entries = chain.get("entries", [])
        return entries[-1]["hash"] if entries else "0" * 64
    return "0" * 64

def append_chain(entry):
    chain = {"last_updated": datetime.now().isoformat(), "entries": []}
    if CHAIN_FILE.exists():
        chain = json.loads(CHAIN_FILE.read_text())
    prev = chain["entries"][-1]["hash"] if chain["entries"] else "0" * 64
    entry["hash"] = hash_entry(prev, {k: entry[k] for k in entry if k != "hash"})
    entry["index"] = len(chain["entries"]) + 1
    chain["entries"].append(entry)
    chain["last_updated"] = datetime.now().isoformat()
    CHAIN_FILE.write_text(json.dumps(chain, ensure_ascii=False, indent=2))

def clean_old_logs():
    """清理30天前的记录"""
    cutoff = (datetime.now() - timedelta(days=30)).isoformat()
    if CHAIN_FILE.exists():
        chain = json.loads(CHAIN_FILE.read_text())
        chain["entries"] = [e for e in chain["entries"] if e.get("time", "") > cutoff]
        CHAIN_FILE.write_text(json.dumps(chain, ensure_ascii=False, indent=2))

def query_stats(hours=24):
    """查询最近N小时的统计"""
    since = int((datetime.now() - timedelta(hours=hours)).timestamp())
    try:
        conn = sqlite3.connect(DB_PATH)
        total = conn.execute("SELECT COUNT(*), SUM(quota) FROM logs WHERE created_at > ?", (since,)).fetchone()
        users = conn.execute("SELECT COUNT(DISTINCT user_id) FROM logs WHERE created_at > ?", (since,)).fetchone()
        ips = conn.execute("SELECT COUNT(DISTINCT ip) FROM logs WHERE created_at > ? AND ip != ''", (since,)).fetchone()
        conn.close()
        return {"total_requests": total[0] or 0, "total_quota": total[1] or 0, "unique_users": users[0] or 0, "unique_ips": ips[0] or 0}
    except:
        return {"total_requests": 0, "total_quota": 0, "unique_users": 0, "unique_ips": 0}

class A12Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "agent": "A12", "chain_entries": len(json.loads(CHAIN_FILE.read_text()).get("entries", [])) if CHAIN_FILE.exists() else 0})
        elif self.path == "/chain":
            data = json.loads(CHAIN_FILE.read_text()) if CHAIN_FILE.exists() else {"entries": []}
            # Return last 50 entries
            data["entries"] = data["entries"][-50:]
            self.send_json(data)
        elif self.path == "/stats":
            stats = query_stats(24)
            stats["audit_chain_entries"] = len(json.loads(CHAIN_FILE.read_text()).get("entries", [])) if CHAIN_FILE.exists() else 0
            self.send_json(stats)
        elif self.path == "/verify":
            # Verify chain integrity
            chain = json.loads(CHAIN_FILE.read_text()) if CHAIN_FILE.exists() else {"entries": []}
            valid = True
            for i in range(1, len(chain["entries"])):
                prev = chain["entries"][i-1]["hash"]
                curr_data = {k: v for k, v in chain["entries"][i].items() if k != "hash"}
                expected = hashlib.sha256((prev + json.dumps(curr_data, sort_keys=True, ensure_ascii=False)).encode()).hexdigest()
                if expected != chain["entries"][i]["hash"]:
                    valid = False
                    break
            self.send_json({"chain_valid": valid, "total_entries": len(chain["entries"])})
        elif self.path == "/clean":
            clean_old_logs()
            self.send_json({"status": "cleaned"})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/log":
            cl = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(cl))
            append_chain(body)
            self.send_json({"status": "logged"})
        else:
            self.send_error(404)

    def send_json(self, data, code=200):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args): pass

def main():
    if not CHAIN_FILE.exists():
        CHAIN_FILE.write_text('{"entries":[],"last_updated":""}')
    HTTPServer(("0.0.0.0", PORT), A12Handler).serve_forever()

if __name__ == "__main__":
    print(f"[A12] Audit Agent :{PORT}")
    main()
