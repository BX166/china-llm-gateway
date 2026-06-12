#!/usr/bin/env python3
"""AICraft A7 - 关键词过滤 Agent v2 · 端口3010"""

import json
import os
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from datetime import datetime
from pathlib import Path

PORT = 3010
NEW_API = "http://127.0.0.1:3000"
ADMIN_KEY = os.environ.get("AICRAFT_ADMIN_KEY", "sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182")
BASE_DIR = Path("/opt/aicraft/regulator")
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
BLOCKED_FILE = LOG_DIR / "a7_blocked.json"
IP_BLOCK_FILE = LOG_DIR / "a7_ip_blocks.json"

# ====== 持久化IP封禁 ======
def load_blocked_ips():
    if IP_BLOCK_FILE.exists():
        return set(json.loads(IP_BLOCK_FILE.read_text()))
    return set()

def save_blocked_ips(blocked):
    IP_BLOCK_FILE.write_text(json.dumps(list(blocked)))

def load_ip_violations():
    vf = LOG_DIR / "a7_violations.json"
    if vf.exists():
        return json.loads(vf.read_text())
    return {}

def save_ip_violations(v):
    (LOG_DIR / "a7_violations.json").write_text(json.dumps(v))

BLOCKED_IPS = load_blocked_ips()
IP_VIOLATIONS = load_ip_violations()

# ====== 敏感词库（10万+规划·当前核心词库+正则） ======
POLITICAL = ["法轮功","台独","藏独","疆独","达赖","热比娅","六四","天安门事件","falun","tiananmen"]
VIOLENCE = ["炸弹制作","恐怖袭击","如何杀人","枪支制造","爆炸物","暗杀","人体炸弹","how to kill","bomb making"]
PORN = ["裸体","色情","援交","av女优","无码","中出","adult video","porn","escort"]
ILLEGAL = ["赌博","博彩","赌场","毒品","冰毒","海洛因","大麻购买","摇头丸","casino","heroin","cocaine"]

ALL_KEYWORDS = set()
for lst in [POLITICAL, VIOLENCE, PORN, ILLEGAL]:
    for w in lst:
        ALL_KEYWORDS.add(w.lower())

PRIVACY_PATTERNS = [
    (r'\b\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b', '身份证号'),
    (r'\b1[3-9]\d{9}\b', '手机号'),
    (r'\b\d{16,19}\b', '银行卡号'),
]

def check_content(text):
    """检查文本·返回 (is_blocked, reason)"""
    if not text or not isinstance(text, str):
        return False, ""
    text_lower = text.lower().strip()
    if len(text_lower) < 2:
        return False, ""

    # 关键词直接匹配
    for word in ALL_KEYWORDS:
        if word in text_lower:
            return True, f"敏感词: {word}"

    # 变体检测: 去除空格和特殊符号后匹配（防止h.e.l.l.o这类绕过）
    clean = re.sub(r'[\s\W_]+', '', text_lower)
    if len(clean) >= 3:
        for word in ALL_KEYWORDS:
            clean_word = re.sub(r'[\s\W_]+', '', word)
            if len(clean_word) >= 3 and clean_word in clean:
                return True, f"敏感词变体: {word}"

    # 隐私信息检测
    for pattern, name in PRIVACY_PATTERNS:
        found = re.findall(pattern, text)
        if found:
            return True, f"隐私泄露: {name} ({len(found)}处)"

    return False, ""

def extract_text(messages):
    if not messages or not isinstance(messages, list):
        return ""
    texts = []
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        content = msg.get("content", "")
        if isinstance(content, str):
            texts.append(content)
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict):
                    t = part.get("text", "") or part.get("content", "")
                    if isinstance(t, str):
                        texts.append(t)
    return " ".join(texts)[:2000]

def log_block(user_id, ip, model, reason, text_snippet):
    entry = {"time": datetime.now().isoformat(), "user_id": user_id or "?", "ip": ip or "?",
             "model": model, "reason": reason, "snippet": (text_snippet or "")[:150]}
    with open(BLOCKED_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def record_violation(ip):
    IP_VIOLATIONS[ip] = IP_VIOLATIONS.get(ip, 0) + 1
    save_ip_violations(IP_VIOLATIONS)
    if IP_VIOLATIONS[ip] >= 3:
        BLOCKED_IPS.add(ip)
        save_blocked_ips(BLOCKED_IPS)
        print(f"[A7] 封禁IP: {ip} (3次违规)")

class A7Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/v1/chat/completions/check"):
            self.send_error(404); return
        try:
            cl = int(self.headers.get("Content-Length", 0))
            if cl == 0: self.send_error(400, "Empty body"); return
            body = json.loads(self.rfile.read(cl))
        except:
            self.send_error(400, "Invalid JSON"); return

        messages = body.get("messages", [])
        model = body.get("model", "?")
        user_ip = self.headers.get("X-Real-IP", self.client_address[0])
        user_id = body.get("user", "?")

        # 已封禁IP
        if user_ip in BLOCKED_IPS:
            self.send_json({"error":{"message":"请求被拒绝","type":"content_filter","code":"ip_blocked"}}, 403); return

        # 内容检查
        text = extract_text(messages)
        blocked, reason = check_content(text)
        if blocked:
            log_block(user_id, user_ip, model, reason, text)
            record_violation(user_ip)
            self.send_json({"error":{"message":"请求包含不适当内容","type":"content_filter","code":"content_blocked","reason":reason}}, 400); return

        # 放行→转发
        try:
            req_body = json.dumps(body).encode("utf-8")
            req = Request(f"{NEW_API}/v1/chat/completions", data=req_body, headers={
                "Content-Type":"application/json", "Authorization":f"Bearer {ADMIN_KEY}"})
            resp = urlopen(req, timeout=60)
            self.send_json(json.loads(resp.read().decode("utf-8")), 200)
        except Exception as e:
            self.send_error(502, str(e))

    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status":"ok","agent":"A7","keywords":len(ALL_KEYWORDS),"blocked_ips":len(BLOCKED_IPS)}, 200)
        elif self.path == "/blocked":
            self.send_json({"blocked_ips":list(BLOCKED_IPS),"violations":dict(IP_VIOLATIONS)}, 200)
        else:
            self.send_error(404)

    def send_json(self, data, code):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.send_header("X-Content-Filter", "A7-PASS" if code==200 else "A7-BLOCK")
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args): pass  # 静默日志

def main():
    HTTPServer(("0.0.0.0", PORT), A7Handler).serve_forever()

if __name__ == "__main__":
    print(f"[A7] 启动 :{PORT} | 关键词:{len(ALL_KEYWORDS)} | 封禁IP:{len(BLOCKED_IPS)}")
    main()
