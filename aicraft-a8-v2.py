#!/usr/bin/env python3
"""AICraft A8 - AI语义审核 Agent v2 · 端口3011"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from datetime import datetime
from pathlib import Path

PORT = 3011
NEW_API = "http://127.0.0.1:3000"
ADMIN_KEY = "sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182"
LOG_DIR = Path("/opt/aicraft/regulator/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES = ["正常","涉政","涉恐","涉黄","涉赌","涉毒","涉暴"]
BLOCKED = {"涉政","涉恐","涉黄","涉毒"}  # 直接拦截
WARN = {"涉赌","涉暴"}  # 标记

REVIEW_PROMPT = """内容安全审核。分类以下用户输入，只回复类别名称:
1.正常(编程/翻译/写作/问答等合法内容)
2.涉政(政治敏感/攻击政府)
3.涉恐(暴力恐怖/武器制造)
4.涉黄(色情低俗)
5.涉赌(赌博博彩)
6.涉毒(毒品相关)
7.涉暴(暴力血腥)

输入: {text}
类别:"""

def classify(text):
    if not text or len(text.strip()) < 3:
        return "正常", 0.0
    try:
        body = json.dumps({"model":"deepseek-chat","messages":[{"role":"user","content":REVIEW_PROMPT.replace("{text}",text[:500])}],"max_tokens":5,"temperature":0}).encode()
        req = Request(f"{NEW_API}/v1/chat/completions", data=body, headers={"Content-Type":"application/json","Authorization":f"Bearer {ADMIN_KEY}"})
        result = json.loads(urlopen(req, timeout=15).read())["choices"][0]["message"]["content"].strip()
        for cat in CATEGORIES:
            if cat in result:
                return cat, 0.9
        return "正常", 0.1
    except Exception as e:
        # 审核故障 → 拒绝请求（不允许绕过审核）
        print(f"[A8] classify failed: {e}")
        return "审核故障", 1.0

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

def log_audit(user_id, ip, model, category, confidence, snippet):
    entry = {"time":datetime.now().isoformat(),"user_id":user_id or "?","ip":ip or "?",
             "model":model,"category":category,"confidence":round(confidence,2),"snippet":(snippet or "")[:150]}
    audit_file = LOG_DIR / f"a8_audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(audit_file, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

class A8Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/v1/chat/completions/review"):
            self.send_error(404); return
        try:
            cl = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(cl))
        except:
            self.send_error(400); return

        messages = body.get("messages", [])
        model = body.get("model", "?")
        user_ip = self.headers.get("X-Real-IP", self.client_address[0])
        user_id = body.get("user", "?")
        text = extract_text(messages)

        start = time.time()
        category, confidence = classify(text)
        latency = int((time.time() - start) * 1000)

        log_audit(user_id, user_ip, model, category, confidence, text)

        # 审核故障
        if category == "审核故障":
            self.send_json({"error":{"message":"安全审核服务暂时不可用","type":"service_error","code":"review_unavailable"}}, 503); return

        # 高危拦截
        if category in BLOCKED:
            self.send_json({"error":{"message":"请求内容未通过安全审核","type":"content_filter","code":"ai_review_blocked","category":category,"latency_ms":latency}}, 400); return

        # 中危标记
        if category in WARN:
            self.send_json({"warning":"content_flagged","category":category,"latency_ms":latency}, 200); return

        # 放行→转发
        try:
            req_body = json.dumps(body).encode("utf-8")
            req = Request(f"{NEW_API}/v1/chat/completions", data=req_body, headers={"Content-Type":"application/json","Authorization":f"Bearer {ADMIN_KEY}"})
            resp_data = json.loads(urlopen(req, timeout=60).read().decode("utf-8"))
            resp_data["aicraft_safety"] = {"agent":"A8","category":category,"confidence":round(confidence,2),"latency_ms":latency}
            self.send_json(resp_data, 200)
        except Exception as e:
            self.send_error(502, str(e))

    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status":"ok","agent":"A8","categories":len(CATEGORIES)}, 200)
        elif self.path == "/stats":
            audit_file = LOG_DIR / f"a8_audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
            count = 0
            if audit_file.exists():
                count = sum(1 for _ in open(audit_file))
            self.send_json({"today_audits":count,"blocked_categories":list(BLOCKED)}, 200)
        else:
            self.send_error(404)

    def send_json(self, data, code):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(resp)))
        self.send_header("X-Safety-Category", data.get("category","N/A") if isinstance(data, dict) else "N/A")
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args): pass

def main():
    print(f"[A8] 启动 :{PORT} | {len(CATEGORIES)}类 | 拦截:{BLOCKED} | 警告:{WARN}")
    HTTPServer(("0.0.0.0", PORT), A8Handler).serve_forever()

if __name__ == "__main__":
    main()
