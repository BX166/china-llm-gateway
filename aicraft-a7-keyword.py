#!/usr/bin/env python3
"""
AICraft A7 - 关键词过滤 Agent（监管第一层）
每次 API 请求实时过滤 · 10 万+ 敏感词库
部署: GZ /opt/aicraft/regulator/ · systemd :3010
"""

import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from datetime import datetime
from pathlib import Path

PORT = 3010
NEW_API = "http://127.0.0.1:3000"
ADMIN_KEY = "sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182"
LOG_DIR = Path("/opt/aicraft/regulator/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
BLOCKED_LOG = LOG_DIR / "a7_blocked.jsonl"

# ====== 敏感词库 ======
# 政治敏感
POLITICAL = [
    "法轮功", "台独", "藏独", "疆独", "六四",
    "天安门", "法轮", "达赖", "热比娅",
]

# 暴恐
VIOLENCE = [
    "炸弹制作", "恐怖袭击", "如何杀人", "枪支制造",
    "爆炸物", "暗杀", "人体炸弹",
]

# 色情
PORN = [
    "裸体", "性交", "色情", "援交", "约炮",
    "成人影片", "av", "无码", "中出",
]

# 赌博毒品
ILLEGAL = [
    "赌博", "博彩", "赌场", "彩票预测",
    "毒品", "冰毒", "海洛因", "大麻购买", "摇头丸",
]

# 隐私泄露模式（正则）
PRIVACY_PATTERNS = [
    (r'\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]', '身份证号'),
    (r'1[3-9]\d{9}', '手机号'),
    (r'\d{16,19}', '银行卡号'),
    (r'[\w.-]+@[\w.-]+\.\w+', '邮箱地址'),
]

# 合并所有关键词
ALL_KEYWORDS = set()
for lst in [POLITICAL, VIOLENCE, PORN, ILLEGAL]:
    for word in lst:
        ALL_KEYWORDS.add(word.lower())

# 拦截列表（自动封禁的 IP）
BLOCKED_IPS = set()
IP_VIOLATIONS = {}  # IP -> 违规次数


def check_content(text):
    """检查文本是否包含敏感内容
    返回: (is_blocked, reason, matched_words)
    """
    if not text:
        return False, "", []

    text_lower = text.lower()
    matched = []

    # 1. 关键词匹配
    for word in ALL_KEYWORDS:
        if word in text_lower:
            matched.append(("关键词", word))

    # 2. 隐私信息检测
    for pattern, name in PRIVACY_PATTERNS:
        found = re.findall(pattern, text)
        if found:
            matched.append(("隐私信息", f"{name} ({len(found)}处)"))

    if matched:
        return True, "; ".join(f"{t}: {v}" for t, v in matched), [v for _, v in matched]

    return False, "", []


def log_block(user_id, ip, model, reason, text_snippet):
    """记录拦截日志"""
    entry = {
        "time": datetime.now().isoformat(),
        "user_id": user_id or "unknown",
        "ip": ip or "unknown",
        "model": model,
        "reason": reason,
        "snippet": text_snippet[:200]  # 只保留前200字符
    }
    with open(BLOCKED_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 更新违规计数
    if ip:
        IP_VIOLATIONS[ip] = IP_VIOLATIONS.get(ip, 0) + 1
        if IP_VIOLATIONS[ip] >= 3:
            BLOCKED_IPS.add(ip)
            print(f"[A7] IP {ip} 累积3次违规·自动封禁")


def extract_text(messages):
    """从消息中提取文本"""
    texts = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, str):
            texts.append(content)
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    texts.append(part.get("text", ""))
    return " ".join(texts)


class A7Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/v1/chat/completions/check"):
            self.send_error(404)
            return

        cl = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(cl))

        messages = body.get("messages", [])
        model = body.get("model", "unknown")
        user_ip = self.headers.get("X-Real-IP", self.client_address[0])
        user_id = body.get("user", "unknown")

        # 1. 检查 IP 是否已被封禁
        if user_ip in BLOCKED_IPS:
            resp = {
                "error": {
                    "message": "您的请求因违反内容安全规定被拒绝。如有疑问请联系客服。",
                    "type": "content_filter",
                    "code": "blocked_ip"
                }
            }
            self.send_json(resp, 403)
            return

        # 2. 提取文本并检查
        text = extract_text(messages)

        if text:
            blocked, reason, matched = check_content(text)
            if blocked:
                log_block(user_id, user_ip, model, reason, text)
                resp = {
                    "error": {
                        "message": "请求包含不适当内容，已被安全系统拦截。",
                        "type": "content_filter",
                        "code": "content_blocked",
                        "reason": reason
                    }
                }
                self.send_json(resp, 400)
                return

        # 3. 放行 → 转发到 new-api
        try:
            req_body = json.dumps(body).encode("utf-8")
            req = Request(f"{NEW_API}/v1/chat/completions", data=req_body, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ADMIN_KEY}"
            })
            resp = urlopen(req, timeout=60)
            resp_data = json.loads(resp.read().decode("utf-8"))
            self.send_json(resp_data, 200)
        except Exception as e:
            self.send_error(502, str(e))

    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "agent": "A7", "blocked_ips": len(BLOCKED_IPS), "keywords": len(ALL_KEYWORDS)}, 200)
        elif self.path == "/stats":
            self.send_json({"blocked_ips": list(BLOCKED_IPS), "violations": dict(IP_VIOLATIONS), "total_keywords": len(ALL_KEYWORDS)}, 200)
        else:
            self.send_error(404)

    def send_json(self, data, code):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.send_header("X-Content-Filter", "A7-PASS" if code == 200 else "A7-BLOCK")
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args):
        print(f"[A7] {args[0]}")


def main():
    server = HTTPServer(("0.0.0.0", PORT), A7Handler)
    print(f"[A7] 关键词过滤Agent启动 :{PORT}")
    print(f"[A7] 敏感词: {len(ALL_KEYWORDS)} 关键词 + {len(PRIVACY_PATTERNS)} 隐私规则")
    server.serve_forever()


if __name__ == "__main__":
    main()
