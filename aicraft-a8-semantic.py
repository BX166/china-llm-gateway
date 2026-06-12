#!/usr/bin/env python3
"""
AICraft A8 - AI 语义审核 Agent（监管第二层）
用 DeepSeek Flash 对每次请求做 7 类安全分类
部署: GZ /opt/aicraft/regulator/ · systemd :3011
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from datetime import datetime
from pathlib import Path

PORT = 3011
NEW_API = "http://127.0.0.1:3000"
A7_API = "http://127.0.0.1:3010"
ADMIN_KEY = "sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182"
LOG_DIR = Path("/opt/aicraft/regulator/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 7 类安全分类
CATEGORIES = ["正常", "涉政", "涉恐", "涉黄", "涉赌", "涉毒", "涉暴"]

# 审核 Prompt
REVIEW_PROMPT = """你是内容安全审核系统。请将以下用户输入分类为以下7类之一。
只回复类别名称，不要解释。

类别:
1. 正常 - 常规编程、翻译、写作、问答等合法内容
2. 涉政 - 涉及政治敏感话题、攻击政府、分裂国家
3. 涉恐 - 涉及暴力恐怖、武器制造、伤害他人
4. 涉黄 - 涉及色情、低俗、性暗示内容
5. 涉赌 - 涉及赌博、博彩相关内容
6. 涉毒 - 涉及毒品相关话题
7. 涉暴 - 涉及暴力、血腥、残忍内容

用户输入: {text}

类别:"""


def classify(text):
    """调用 DeepSeek Flash 做安全分类"""
    if not text or len(text.strip()) < 2:
        return "正常", 0.0

    prompt = REVIEW_PROMPT.replace("{text}", text[:500])

    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 5,
        "temperature": 0
    }).encode()

    try:
        req = Request(f"{NEW_API}/v1/chat/completions", data=body, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ADMIN_KEY}"
        })
        resp = json.loads(urlopen(req, timeout=10).read())
        result = resp["choices"][0]["message"]["content"].strip()

        # 匹配分类
        for cat in CATEGORIES:
            if cat in result:
                return cat, 0.9

        return "正常", 0.1  # 无法分类 → 默认正常
    except Exception as e:
        print(f"[A8] 分类失败: {e}")
        return "正常", 0.0  # API 故障 → 放行（避免误杀）


def extract_text(messages):
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


def log_audit(user_id, ip, model, category, confidence, text_snippet):
    entry = {
        "time": datetime.now().isoformat(),
        "user_id": user_id or "unknown",
        "ip": ip or "unknown",
        "model": model,
        "category": category,
        "confidence": round(confidence, 2),
        "snippet": text_snippet[:200]
    }
    audit_file = LOG_DIR / f"a8_audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(audit_file, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class A8Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/v1/chat/completions/review"):
            self.send_error(404)
            return

        cl = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(cl))

        messages = body.get("messages", [])
        model = body.get("model", "unknown")
        user_ip = self.headers.get("X-Real-IP", self.client_address[0])
        user_id = body.get("user", "unknown")
        text = extract_text(messages)

        # AI 安全分类
        start = time.time()
        category, confidence = classify(text)
        latency = int((time.time() - start) * 1000)

        log_audit(user_id, user_ip, model, category, confidence, text)

        # 高危分类 → 拦截
        BLOCKED_CATEGORIES = ["涉政", "涉恐", "涉黄", "涉毒"]
        if category in BLOCKED_CATEGORIES:
            resp = {
                "error": {
                    "message": "请求内容未通过安全审核。",
                    "type": "content_filter",
                    "code": "ai_review_blocked",
                    "category": category,
                    "latency_ms": latency
                }
            }
            self.send_json(resp, 400)
            return

        # 中危 → 标记但放行
        if category in ["涉赌", "涉暴"]:
            self.send_json({"warning": "content_flagged", "category": category}, 200)
            return

        # 正常 → 转发到 A7 或 new-api
        try:
            req_body = json.dumps(body).encode("utf-8")
            req = Request(f"{NEW_API}/v1/chat/completions", data=req_body, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ADMIN_KEY}"
            })
            resp = urlopen(req, timeout=60)
            resp_data = json.loads(resp.read().decode("utf-8"))
            resp_data["aicraft_safety"] = {"category": category, "confidence": confidence, "latency_ms": latency}
            self.send_json(resp_data, 200)
        except Exception as e:
            self.send_error(502, str(e))

    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "agent": "A8", "categories": len(CATEGORIES)}, 200)
        elif self.path == "/stats":
            audit_file = LOG_DIR / f"a8_audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
            count = 0
            if audit_file.exists():
                count = len(audit_file.read_text().strip().split("\n")) if audit_file.read_text().strip() else 0
            self.send_json({"today_audits": count, "categories": CATEGORIES}, 200)
        else:
            self.send_error(404)

    def send_json(self, data, code):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.send_header("X-Safety-Category", data.get("category", "unknown") if isinstance(data, dict) else "N/A")
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args):
        print(f"[A8] {args[0]}")


def main():
    server = HTTPServer(("0.0.0.0", PORT), A8Handler)
    print(f"[A8] 语义审核Agent启动 :{PORT}")
    print(f"[A8] 分类维度: {len(CATEGORIES)}类 | 拦截: 涉政/涉恐/涉黄/涉毒")
    server.serve_forever()


if __name__ == "__main__":
    main()
