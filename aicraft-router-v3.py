#!/usr/bin/env python3
"""AICraft Auto Router v3 — 人性化 · 分简单/复杂 · 记偏好"""

import json
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from pathlib import Path

NEW_API = "http://127.0.0.1:3000"
ADMIN_KEY = os.environ.get("AICRAFT_ADMIN_KEY", "sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182")
PREF_DIR = Path("/opt/aicraft/router/prefs")
PREF_DIR.mkdir(parents=True, exist_ok=True)

# 路由表：每类任务有 简单(便宜) 和 复杂(质量) 两个选择
ROUTES = {
    "coding": {
        "simple": {"model": "deepseek-chat", "why": "简单代码用DeepSeek就够了·便宜快速"},
        "complex": {"model": "deepseek-chat", "why": "复杂算法用DeepSeek V3·代码能力全球第一"},
    },
    "translation": {
        "simple": {"model": "qwen-turbo", "why": "日常翻译用轻量模型·性价比最高"},
        "complex": {"model": "qwen-max", "why": "专业翻译用增强模型·更准确"},
    },
    "chinese": {
        "simple": {"model": "qwen-turbo", "why": "简单中文用轻量模型"},
        "complex": {"model": "qwen-max", "why": "长文中用Qwen-Max·中文理解最好"},
    },
    "reasoning": {
        "simple": {"model": "qwen-turbo", "why": "日常逻辑用轻量模型"},
        "complex": {"model": "glm-5", "why": "复杂推理用GLM-5·逻辑链最清晰"},
    },
    "creative": {
        "simple": {"model": "deepseek-chat", "why": "简短创意用DeepSeek"},
        "complex": {"model": "minimax-m2.5", "why": "深度创作用MiniMax M2.5·文学性最好"},
    },
    "chat": {
        "simple": {"model": "qwen-turbo", "why": "日常聊天用轻量模型"},
        "complex": {"model": "doubao-pro", "why": "需要亲和力的对话用豆包Pro"},
    },
}

CLASSIFIER = """Classify this user request into ONE category. Reply with only the category name.

coding: programming, debugging, algorithms, code
translation: translate, summarize, rewrite, batch
chinese: Chinese content, multilingual, China-specific
reasoning: math, logic, analysis, complex problems
creative: writing, stories, poetry, scripts
chat: conversation, Q&A, casual talk

User: {msg}
Category:"""


def get_complexity(messages):
    """判断任务复杂度：简单/复杂"""
    total_len = sum(len(m.get("content", "")) for m in messages if isinstance(m, dict))
    msg_count = len([m for m in messages if isinstance(m, dict) and m.get("role") == "user"])

    # 复杂任务特征
    if total_len > 1000: return "complex"
    if msg_count > 5: return "complex"
    if any(kw in str(messages).lower() for kw in ["explain", "analyze", "compare", "为什么", "详细", "分析"]):
        return "complex"

    return "simple"


def classify(messages):
    """分类用户任务"""
    text = ""
    for m in messages:
        if isinstance(m, dict) and m.get("role") == "user":
            text = m.get("content", "")[-800:]
    if not text: return "chat"

    body = json.dumps({"model": "deepseek-chat", "messages": [
        {"role": "user", "content": CLASSIFIER.replace("{msg}", text)}
    ], "max_tokens": 6, "temperature": 0}).encode()

    try:
        req = Request(f"{NEW_API}/v1/chat/completions", data=body,
                      headers={"Content-Type": "application/json", "Authorization": f"Bearer {ADMIN_KEY}"})
        result = json.loads(urlopen(req, timeout=10).read())["choices"][0]["message"]["content"].strip().lower()
        for cat in ROUTES:
            if cat in result: return cat
        return "chat"
    except:
        return "chat"


def get_user_pref(user_id):
    """读取用户偏好"""
    f = PREF_DIR / f"{user_id}.json"
    if f.exists():
        return json.loads(f.read_text())
    return {"manual_overrides": {}, "last_used": {}}


def save_user_pref(user_id, pref):
    (PREF_DIR / f"{user_id}.json").write_text(json.dumps(pref, ensure_ascii=False, indent=2))


def learn_preference(user_id, user_model, auto_model):
    """学习用户偏好：如果用户手动改了模型，记录"""
    if not user_id or user_id == "?": return
    pref = get_user_pref(user_id)
    if user_model and user_model != "auto" and user_model != auto_model:
        pref["manual_overrides"][user_model] = pref["manual_overrides"].get(user_model, 0) + 1
    save_user_pref(user_id, pref)


def route(messages, user_model=None, user_id=None):
    """路由决策 v3"""
    # 用户指定了模型 → 直接使用（记偏好）
    if user_model and user_model != "auto":
        learn_preference(user_id, user_model, user_model)
        return user_model, {"mode": "manual", "why": "您选择的模型"}

    # 查用户偏好
    pref = get_user_pref(user_id) if user_id else {}
    if pref.get("manual_overrides"):
        top_model = max(pref["manual_overrides"], key=pref["manual_overrides"].get)
        if pref["manual_overrides"][top_model] >= 3:
            # 用户连续3次手动选同一个模型 → 记住偏好
            return top_model, {"mode": "preferred", "why": f"根据您的使用习惯，为您选择 {top_model}"}

    # 自动路由
    start = time.time()
    category = classify(messages)
    complexity = get_complexity(messages)
    tier = "complex" if complexity == "complex" else "simple"
    route_info = ROUTES.get(category, ROUTES["chat"])
    choice = route_info[tier]
    latency = int((time.time() - start) * 1000)

    return choice["model"], {
        "mode": "auto",
        "category": category,
        "complexity": complexity,
        "model": choice["model"],
        "why": choice["why"],
        "latency_ms": latency,
        "cost": "~$0.00003" if complexity == "simple" else "~$0.00005",
    }


class RouterHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/v1/chat/completions/auto"):
            self.send_error(404); return

        cl = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(cl))
        model = body.get("model", "auto")
        messages = body.get("messages", [])
        user_id = body.get("user") or self.headers.get("X-User-ID", "?")

        target, info = route(messages, user_model=model, user_id=user_id)

        # Forward
        body["model"] = target
        try:
            req = Request(f"{NEW_API}/v1/chat/completions", data=json.dumps(body).encode(),
                          headers={"Content-Type": "application/json", "Authorization": f"Bearer {ADMIN_KEY}"})
            resp_data = json.loads(urlopen(req, timeout=60).read().decode("utf-8"))
            resp_data["aicraft_routing"] = info
            resp_data["aicraft_routing"]["routed_to"] = target
        except Exception as e:
            resp_data = {"error": str(e), "aicraft_routing": info}

        resp_bytes = json.dumps(resp_data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.send_header("X-AICraft-Routed-To", target)
        why = info.get("why", "?")[:80].encode("ascii", "ignore").decode("ascii")
        self.send_header("X-AICraft-Mode", info.get("mode", "?"))
        self.send_header("X-AICraft-Why", why if why else "auto-routed")
        self.end_headers()
        self.wfile.write(resp_bytes)

    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "router": "v3", "features": ["simple_vs_complex", "preference_learning", "human_friendly"]})
        elif self.path == "/routes":
            self.send_json(ROUTES)
        elif self.path.startswith("/prefs/"):
            uid = self.path.split("/")[-1]
            self.send_json(get_user_pref(uid))
        else:
            self.send_error(404)

    def send_json(self, data):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args): pass


def main():
    HTTPServer(("0.0.0.0", 3001), RouterHandler).serve_forever()

if __name__ == "__main__":
    print("[Router v3] Starting :3001 — 人性化 · 简单/复杂 · 记偏好")
    main()
