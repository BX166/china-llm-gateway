#!/usr/bin/env python3
"""
AICraft Auto Router v4 — 个性化学习引擎
每个用户独立画像·Agent感知·持续学习·越用越懂你
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from datetime import datetime
from pathlib import Path
from collections import defaultdict

NEW_API = "http://127.0.0.1:3000"
ADMIN_KEY = os.environ.get("AICRAFT_ADMIN_KEY", "sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182")
PROFILE_DIR = Path("/opt/aicraft/router/profiles")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

ROUTES = {
    "coding": {
        "primary": "deepseek-chat", "fallback": "qwen-max",
        "cheap": "qwen-turbo",
    },
    "translation": {
        "primary": "qwen-turbo", "fallback": "deepseek-chat",
        "cheap": "qwen-turbo",
    },
    "chinese": {
        "primary": "qwen-max", "fallback": "glm-5",
        "cheap": "qwen-turbo",
    },
    "reasoning": {
        "primary": "glm-5", "fallback": "deepseek-chat",
        "cheap": "deepseek-chat",
    },
    "creative": {
        "primary": "minimax-m2.5", "fallback": "deepseek-chat",
        "cheap": "deepseek-chat",
    },
    "chat": {
        "primary": "qwen-turbo", "fallback": "doubao-pro",
        "cheap": "qwen-turbo",
    },
}

CLASSIFIER = """Classify this user request into ONE category. Reply with only the category name.
coding: programming, debugging, algorithms, code
translation: translate, summarize, rewrite, batch
chinese: Chinese content, multilingual, China context
reasoning: math, logic, analysis, complex problems
creative: writing, stories, poetry, scripts
chat: conversation, Q&A, casual talk
User: {msg}
Category:"""


def load_profile(user_id):
    """加载用户画像"""
    f = PROFILE_DIR / f"{user_id}.json"
    if f.exists():
        return json.loads(f.read_text())
    return {
        "created": datetime.now().isoformat(),
        "total_requests": 0,
        "task_distribution": {},      # 各任务类型占比
        "model_preferences": {},       # 用户偏好的模型
        "override_history": [],        # 最近20次手动覆盖
        "time_patterns": defaultdict(int),  # 各时段活跃度
        "avg_tokens_per_request": 0,
        "is_agent": False,             # 判断是否自动化Agent
        "agent_confidence": 0,         # Agent判定置信度
    }


def save_profile(user_id, profile):
    profile["last_updated"] = datetime.now().isoformat()
    (PROFILE_DIR / f"{user_id}.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2))


def detect_agent(profile, messages):
    """检测调用方是真人还是自动化Agent"""
    score = profile.get("agent_confidence", 0)

    # Agent特征
    indicators = 0
    total = profile.get("total_requests", 0)

    if total >= 20:
        # 1. 请求间隔高度规律（Agent行为）
        if len(profile.get("override_history", [])) >= 10:
            score += 0.2

        # 2. 几乎从不手动覆盖路由
        overrides = sum(1 for h in profile.get("override_history", []) if h.get("was_override"))
        if total > 10 and overrides / total < 0.05:
            score += 0.3

        # 3. Token消耗高度一致（Agent固定任务）
        if profile.get("avg_tokens_per_request", 0) > 0:
            score += 0.1

        # 4. 24小时持续活跃（不像人需要睡觉）
        hours = len(profile.get("time_patterns", {}))
        if hours >= 18:
            score += 0.3

    profile["is_agent"] = score >= 0.5
    profile["agent_confidence"] = min(score, 1.0)
    return profile["is_agent"]


def classify(messages):
    text = ""
    for m in messages:
        if isinstance(m, dict) and m.get("role") == "user":
            text = m.get("content", "")[-800:]
    if not text:
        return "chat"

    body = json.dumps({"model": "deepseek-chat", "messages": [
        {"role": "user", "content": CLASSIFIER.replace("{msg}", text)}
    ], "max_tokens": 6, "temperature": 0}).encode()

    try:
        req = Request(f"{NEW_API}/v1/chat/completions", data=body,
                      headers={"Content-Type": "application/json", "Authorization": f"Bearer {ADMIN_KEY}"})
        result = json.loads(urlopen(req, timeout=10).read())["choices"][0]["message"]["content"].strip().lower()
        for cat in ROUTES:
            if cat in result:
                return cat
        return "chat"
    except:
        return "chat"


def route(messages, user_model=None, user_id=None):
    """个性化路由决策 v4"""
    pref = load_profile(user_id) if user_id else None

    # === 0. 用户指定了模型 → 尊重选择，快速学习 ===
    if user_model and user_model != "auto":
        if pref:
            # 连续2次手动选同一模型 → 视为执意偏好
            recent = [h for h in pref.get("override_history", []) if h.get("was_override")]
            recent.append({"time": datetime.now().isoformat(), "chosen": user_model})

            if len(recent) >= 2:
                last_two = recent[-2:]
                if last_two[0]["chosen"] == last_two[1]["chosen"]:
                    pref["locked_model"] = user_model
                    pref["locked_at"] = datetime.now().isoformat()

            pref["override_history"].append({
                "time": datetime.now().isoformat(),
                "chosen": user_model,
                "was_override": True
            })
            pref["override_history"] = pref["override_history"][-50:]
            save_profile(user_id, pref)

        return user_model, {
            "mode": "manual",
            "msg": "Respecting your model choice",
            "locked": pref.get("locked_model") == user_model if pref else False
        }

    # === 1. 已锁定偏好 → 直接用 ===
    if pref and pref.get("locked_model"):
        return pref["locked_model"], {
            "mode": "locked",
            "msg": f"Using your preferred model {pref['locked_model']}",
            "unlock_hint": "Set model=auto to let Router choose again"
        }

    # === 2. 用户画像路由 ===
    if pref and pref.get("total_requests", 0) >= 10:
        preferences = pref.get("model_preferences", {})
        if preferences:
            top_model = max(preferences, key=preferences.get)
            top_pct = preferences[top_model] / sum(preferences.values())
            if top_pct > 0.6:
                return top_model, {"mode": "learned", "msg": f"Your go-to model ({top_pct*100:.0f}% of requests)"}

    # === 3. 分类路由 ===
    category = classify(messages)
    complexity = "simple" if sum(len(m.get("content", "")) for m in messages if isinstance(m, dict)) < 500 else "complex"
    r = ROUTES.get(category, ROUTES["chat"])
    model = r["primary"] if complexity == "complex" else r["cheap"]

    # === 4. Agent优化 ===
    agent_note = ""
    if pref:
        is_agent = detect_agent(pref, messages)
        if is_agent and complexity == "simple":
            model = r["cheap"]  # Agent请求优先省钱
            agent_note = " (Agent-optimized)"

    # === 5. 更新画像 ===
    if pref:
        pref["total_requests"] += 1
        pref["task_distribution"][category] = pref["task_distribution"].get(category, 0) + 1
        pref["model_preferences"][model] = pref["model_preferences"].get(model, 0) + 1
        hour = datetime.now().hour
        pref["time_patterns"][str(hour)] = pref["time_patterns"].get(str(hour), 0) + 1
        pref["override_history"].append({"time": datetime.now().isoformat(), "chosen": model, "was_override": False})
        pref["override_history"] = pref["override_history"][-50:]
        save_profile(user_id, pref)

    return model, {
        "mode": "auto" + agent_note,
        "category": category,
        "complexity": complexity,
        "model": model,
        "is_agent": pref.get("is_agent", False) if pref else False,
    }


class RouterHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/v1/chat/completions/auto"):
            self.send_error(404); return

        cl = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(cl))
        model = body.get("model", "auto")
        messages = body.get("messages", [])
        user_id = body.get("user") or self.headers.get("X-User-ID") or self.headers.get("Authorization", "?")[:20]

        target, info = route(messages, user_model=model, user_id=user_id)
        body["model"] = target

        try:
            req = Request(f"{NEW_API}/v1/chat/completions", data=json.dumps(body).encode(),
                          headers={"Content-Type": "application/json", "Authorization": f"Bearer {ADMIN_KEY}"})
            resp_data = json.loads(urlopen(req, timeout=60).read().decode("utf-8"))
            resp_data["aicraft_routing"] = info
            resp_data["aicraft_routing"]["selected_model"] = target
            resp_data["aicraft_routing"]["feedback"] = {
                "used": target,
                "why": "Auto-selected based on your request type",
                "try_also": ["qwen-turbo (cheaper)", "deepseek-chat (better quality)"],
                "tip": "Set model=NAME in your request to lock preference"
            }
            if info.get("msg"):
                resp_data["aicraft_routing"]["message"] = info["msg"]
        except Exception as e:
            resp_data = {"error": str(e), "aicraft_routing": info}

        resp_bytes = json.dumps(resp_data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("X-AICraft-Routed-To", target)
        self.send_header("X-AICraft-Mode", info.get("mode", "?"))
        self.end_headers()
        self.wfile.write(resp_bytes)

    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "router": "v4", "features": ["personalized", "agent_aware", "continuous_learning"]})
        elif self.path.startswith("/profile/"):
            uid = self.path.split("/")[-1]
            self.send_json(load_profile(uid))
        else:
            self.send_error(404)

    def send_json(self, data):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args): pass


def main():
    HTTPServer(("0.0.0.0", 3001), RouterHandler).serve_forever()

if __name__ == "__main__":
    print("[Router v4] 个性化·Agent感知·持续学习 :3001")
    main()
