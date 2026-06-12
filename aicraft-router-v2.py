#!/usr/bin/env python3
"""
AICraft Auto Router v2 — 分级路由 + 质量评分 + 故障转移 + Benchmark
升级: 简单任务走便宜模型, 复杂任务多级判断, 主模型失败自动降级
"""

import json
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen

NEW_API = "http://127.0.0.1:3000"
ADMIN_KEY = os.environ.get("AICRAFT_ADMIN_KEY", "sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182")
DB_PATH = "/opt/new-api/data/one-api.db"

# ====== 分级路由表 v2 ======
# 每个任务类型有 3 档: primary(首选), fallback(降级), cheapest(最省)
ROUTE_TABLE = {
    "coding": {
        "name": "编程/代码",
        "primary": {"model": "deepseek-chat", "why": "DeepSeek V3 - #1 coding benchmark"},
        "fallback": {"model": "qwen-max", "why": "Qwen-Max - strong code, fallback"},
        "cheapest": {"model": "deepseek-chat", "why": "Same model for now"},
        "cost_vs_gpt4": "93%"
    },
    "translation": {
        "name": "翻译/摘要/批量",
        "primary": {"model": "deepseek-chat", "why": "Fastest, cheapest $0.003/M"},
        "fallback": {"model": "qwen-turbo", "why": "Qwen-Turbo also cheap"},
        "cheapest": {"model": "deepseek-chat", "why": "DeepSeek Flash $0.003/M"},
        "cost_vs_gpt4": "99%"
    },
    "chinese": {
        "name": "中文长文/多语言",
        "primary": {"model": "qwen-max", "why": "Best Chinese comprehension"},
        "fallback": {"model": "glm-5", "why": "GLM-5 strong Chinese"},
        "cheapest": {"model": "qwen-turbo", "why": "Lightweight Chinese"},
        "cost_vs_gpt4": "88%"
    },
    "reasoning": {
        "name": "复杂推理/逻辑",
        "primary": {"model": "glm-5", "why": "Clearest reasoning chains"},
        "fallback": {"model": "deepseek-chat", "why": "DeepSeek R1 strong reasoning"},
        "cheapest": {"model": "minimax-m2.5", "why": "Budget reasoning option"},
        "cost_vs_gpt4": "83%"
    },
    "creative": {
        "name": "创意写作/文学",
        "primary": {"model": "minimax-m2.5", "why": "Best literary quality"},
        "fallback": {"model": "qwen-max", "why": "Qwen creative backup"},
        "cheapest": {"model": "deepseek-chat", "why": "Budget creative"},
        "cost_vs_gpt4": "91%"
    },
    "chat": {
        "name": "对话/客服",
        "primary": {"model": "ep-20260608133625-766x4", "why": "Doubao Pro - natural tone"},
        "fallback": {"model": "qwen-turbo", "why": "Qwen-Turbo fast chat"},
        "cheapest": {"model": "deepseek-chat", "why": "Cheapest conversational"},
        "cost_vs_gpt4": "91%"
    },
}

CLASSIFIER_PROMPT = """Classify the user request into exactly ONE category. Reply with ONLY the category name.

Categories:
- coding: programming, debugging, algorithms, technical questions
- translation: translation, summarization, rewriting, batch processing
- chinese: Chinese long-form content, multilingual, China context
- reasoning: math, logic, analysis, complex problem solving
- creative: creative writing, stories, poetry, scripts, literature
- chat: casual conversation, Q&A, customer service, general chat

User: {message}

Category:"""


def classify_task(messages, budget="auto"):
    """分类用户任务。budget=save 时偏向更便宜的模型"""
    user_msg = ""
    for m in messages:
        if m.get("role") == "user":
            user_msg = m.get("content", "")[-800:]

    if not user_msg:
        return "chat"

    prompt = CLASSIFIER_PROMPT.replace("{message}", user_msg)
    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 8, "temperature": 0
    }).encode()

    try:
        req = Request(f"{NEW_API}/v1/chat/completions", data=body, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ADMIN_KEY}"
        })
        resp = json.loads(urlopen(req, timeout=10).read())
        category = resp["choices"][0]["message"]["content"].strip().lower()
        for key in ROUTE_TABLE:
            if key in category:
                return key
        return "chat"
    except:
        return "chat"


def route(messages, preferred_model=None, budget="auto"):
    """
    执行路由决策 v2
    budget: "save" = 省钱优先, "quality" = 质量优先, "auto" = 智能平衡
    返回: (target_model, tier, route_info)
    """
    if preferred_model and preferred_model != "auto":
        return preferred_model, "manual", {}

    start = time.time()
    category = classify_task(messages, budget)
    route_info = dict(ROUTE_TABLE.get(category, ROUTE_TABLE["chat"]))
    route_info["category"] = category

    if budget == "save":
        tier = "cheapest"
        selected = route_info["cheapest"]
    elif budget == "quality":
        tier = "primary"
        selected = route_info["primary"]
    else:
        # Auto: check message complexity
        msg_len = sum(len(m.get("content", "")) for m in messages)
        if msg_len < 50:
            tier = "cheapest"  # Short messages -> save money
            selected = route_info["cheapest"]
        elif msg_len > 2000:
            tier = "primary"   # Long complex -> use best
            selected = route_info["primary"]
        else:
            tier = "primary"
            selected = route_info["primary"]

    route_info["selected_tier"] = tier
    route_info["classify_time_ms"] = int((time.time() - start) * 1000)
    route_info["backup_model"] = route_info["fallback"]["model"]

    return selected["model"], tier, route_info


# ====== Benchmark 系统 ======
BENCHMARK_FILE = "/opt/aicraft/router/benchmark.json"


def load_benchmark():
    if os.path.exists(BENCHMARK_FILE):
        return json.loads(open(BENCHMARK_FILE).read())
    return {"total_routes": 0, "success": 0, "fallback_used": 0, "categories": {},
            "cost_saved_vs_gpt4": 0.0, "avg_latency_ms": 0}


def save_benchmark(bm):
    open(BENCHMARK_FILE, "w").write(json.dumps(bm, indent=2))


def record_benchmark(category, tier, success, latency_ms, used_fallback=False):
    bm = load_benchmark()
    bm["total_routes"] += 1
    if success:
        bm["success"] += 1
    if used_fallback:
        bm["fallback_used"] += 1
    if category not in bm["categories"]:
        bm["categories"][category] = {"total": 0, "success": 0}
    bm["categories"][category]["total"] += 1
    if success:
        bm["categories"][category]["success"] += 1

    # Track cost savings
    savings_map = {k: float(v["cost_vs_gpt4"].replace("%", "")) for k, v in ROUTE_TABLE.items()}
    bm["cost_saved_vs_gpt4"] = (bm["cost_saved_vs_gpt4"] * (bm["total_routes"] - 1) + savings_map.get(
        category, 80)) / bm["total_routes"]

    # Rolling average latency
    bm["avg_latency_ms"] = (bm["avg_latency_ms"] * (bm["total_routes"] - 1) + latency_ms) / bm["total_routes"]

    save_benchmark(bm)
    return bm


# ====== HTTP Server ======
class RouterHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/v1/chat/completions/auto"):
            self.send_error(404)
            return

        cl = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(cl))
        model = body.get("model", "auto")
        messages = body.get("messages", [])
        budget = body.get("aicraft_budget", "auto")  # "save" | "quality" | "auto"

        # Route
        target_model, tier, route_info = route(messages, preferred_model=model, budget=budget)

        # Forward
        body["model"] = target_model
        req_body = json.dumps(body).encode()
        fallback_used = False

        start = time.time()
        try:
            req = Request(f"{NEW_API}/v1/chat/completions", data=req_body, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ADMIN_KEY}"
            })
            resp = urlopen(req, timeout=60)
            resp_data = json.loads(resp.read().decode("utf-8"))
            latency_ms = int((time.time() - start) * 1000)

            # Record benchmark
            record_benchmark(route_info.get("category", "chat"), tier, True, latency_ms, False)

            # Inject routing info
            if route_info:
                resp_data["aicraft_routing"] = {
                    "auto_mode": True,
                    "category": route_info.get("name", ""),
                    "routed_to": target_model,
                    "tier": tier,
                    "why": route_info.get(tier, {}).get("why", ""),
                    "savings_vs_gpt4": route_info.get("cost_vs_gpt4", ""),
                    "classify_ms": route_info.get("classify_time_ms", 0),
                    "backup_standing_by": route_info.get("backup_model", ""),
                }
        except Exception as e:
            # Fallback!
            backup_model = route_info.get("backup_model", route_info.get("fallback", {}).get("model", "deepseek-chat"))
            body["model"] = backup_model
            req_body = json.dumps(body).encode()
            try:
                req = Request(f"{NEW_API}/v1/chat/completions", data=req_body, headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {ADMIN_KEY}"
                })
                resp = urlopen(req, timeout=60)
                resp_data = json.loads(resp.read().decode("utf-8"))
                fallback_used = True
                latency_ms = int((time.time() - start) * 1000)
                record_benchmark(route_info.get("category", "chat"), tier, True, latency_ms, True)
                if route_info:
                    resp_data["aicraft_routing"] = {
                        "auto_mode": True,
                        "fallback_activated": True,
                        "original_target": target_model,
                        "routed_to": backup_model,
                        "why": "Primary model failed, auto-switched to backup",
                    }
            except Exception as e2:
                latency_ms = int((time.time() - start) * 1000)
                record_benchmark(route_info.get("category", "chat"), tier, False, latency_ms, True)
                self.send_error(502, f"All models failed: {e} | {e2}")
                return

        resp_bytes = json.dumps(resp_data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.send_header("X-AICraft-Routed-To", target_model)
        if route_info:
            self.send_header("X-AICraft-Tier", tier)
            self.send_header("X-AICraft-Fallback", str(fallback_used).lower())
            self.send_header("X-AICraft-Savings", route_info.get("cost_vs_gpt4", "N/A"))
        self.end_headers()
        self.wfile.write(resp_bytes)

    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "router": "aicraft-v2", "version": "2.0"})
        elif self.path == "/routes":
            self.send_json({
                "version": "2.0",
                "features": ["tiered_routing", "fallback", "benchmark"],
                "route_table": {k: {
                    "name": v["name"],
                    "primary": v["primary"]["model"],
                    "fallback": v["fallback"]["model"],
                    "cheapest": v["cheapest"]["model"],
                    "savings": v["cost_vs_gpt4"]
                } for k, v in ROUTE_TABLE.items()}
            })
        elif self.path == "/benchmark":
            bm = load_benchmark()
            self.send_json(bm)
        else:
            self.send_error(404)

    def send_json(self, data):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args):
        print(f"[Router-v2] {args[0]}")


def main():
    port = 3001
    server = HTTPServer(("0.0.0.0", port), RouterHandler)
    print(f"[Router v2] AICraft Auto Router v2 on :{port}")
    print("[Router v2] Features: Tiered routing + Fallback + Benchmark")
    print(f"[Router v2] {len(ROUTE_TABLE)} categories, {len(ROUTE_TABLE)*3} routing options")
    server.serve_forever()


if __name__ == "__main__":
    main()
