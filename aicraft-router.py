#!/usr/bin/env python3
"""
AICraft Auto Router — 智能模型路由
按计划书5AB.1: 用DeepSeek V4-Flash做任务分类 → 自动选最优模型
部署: 广州 /opt/aicraft/router/
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen

# 本地 new-api 地址
NEW_API = "http://127.0.0.1:3000"
ADMIN_KEY = "sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182"
CLASSIFIER_MODEL = "deepseek-chat"  # 用DeepSeek分类，最便宜

# 路由表 — 按计划书5AB.1
ROUTE_MAP = {
    "编程/代码": {
        "model": "deepseek-chat",
        "why": "代码能力全球第一·$0.35/M",
        "cost_vs_gpt4": "节省93%"
    },
    "翻译/摘要/批量": {
        "model": "deepseek-chat",
        "why": "最便宜·量大不心疼·$0.003/M",
        "cost_vs_gpt4": "节省99%"
    },
    "中文长文/多语言": {
        "model": "qwen-max",
        "why": "中文理解最好·阿里生态",
        "cost_vs_gpt4": "节省88%"
    },
    "复杂推理/逻辑": {
        "model": "glm-5",
        "why": "逻辑链最清晰·$0.87/M",
        "cost_vs_gpt4": "节省83%"
    },
    "创意写作/文学": {
        "model": "minimax-m2.5",
        "why": "文学性最好·海外爆火",
        "cost_vs_gpt4": "节省91%"
    },
    "对话/客服": {
        "model": "ep-20260608133625-766x4",
        "why": "亲和力最佳·字节生态·$0.43/M",
        "cost_vs_gpt4": "节省91%"
    },
}

CLASSIFIER_PROMPT = """你是一个任务分类器。请把用户请求分成以下6类之一，只回复类别名称，不要解释：

类别：
1. 编程/代码 — 写代码、debug、技术问题、算法
2. 翻译/摘要/批量 — 翻译、摘要、改写、批量处理
3. 中文长文/多语言 — 中文长文章、多语言混合、中国语境
4. 复杂推理/逻辑 — 数学、逻辑推理、分析论证
5. 创意写作/文学 — 文学创作、故事、诗歌、剧本
6. 对话/客服 — 闲聊、问答、客服对话

用户请求: {user_message}

类别:"""


def classify_task(messages):
    """用廉价模型分类用户任务"""
    # 取最后一条用户消息
    user_msg = ""
    for m in messages:
        if m.get("role") == "user":
            user_msg = m.get("content", "")[-500:]  # 只用最后500字符

    if not user_msg:
        return "对话/客服"

    prompt = CLASSIFIER_PROMPT.replace("{user_message}", user_msg)

    body = json.dumps({
        "model": CLASSIFIER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 10,
        "temperature": 0
    }).encode()

    try:
        req = Request(f"{NEW_API}/v1/chat/completions", data=body, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ADMIN_KEY}"
        })
        resp = json.loads(urlopen(req, timeout=15).read())
        category = resp["choices"][0]["message"]["content"].strip()
        # 模糊匹配
        for key in ROUTE_MAP:
            if key[:4] in category or category[:4] in key:
                return key
        return "对话/客服"  # 默认
    except Exception as e:
        print(f"[Router] 分类失败: {e}, 使用默认路由")
        return "对话/客服"


def route(messages, preferred_model=None):
    """
    执行路由决策
    返回: (target_model, route_info)
    """
    # 如果用户指定了模型，直接使用（不走Auto）
    if preferred_model and preferred_model != "auto":
        return preferred_model, None

    # Auto模式: 分类+路由
    start = time.time()
    category = classify_task(messages)
    route_info = ROUTE_MAP.get(category, ROUTE_MAP["对话/客服"])
    route_info["category"] = category
    route_info["classify_time_ms"] = int((time.time() - start) * 1000)
    return route_info["model"], route_info


class RouterHandler(BaseHTTPRequestHandler):
    """Auto Router API endpoint — /v1/chat/completions with model=auto"""

    def do_POST(self):
        if self.path not in ("/v1/chat/completions", "/v1/chat/completions/auto"):
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        model = body.get("model", "auto")
        messages = body.get("messages", [])

        # 路由决策
        target_model, route_info = route(messages, preferred_model=model)

        # 转发请求到目标模型
        body["model"] = target_model

        req_body = json.dumps(body).encode()
        req = Request(f"{NEW_API}/v1/chat/completions", data=req_body, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ADMIN_KEY}"
        })

        try:
            resp = urlopen(req, timeout=60)
            resp_body = resp.read()
            resp_data = json.loads(resp_body.decode("utf-8"))

            # 注入路由信息到响应
            if route_info:
                resp_data["aicraft_routing"] = {
                    "auto_mode": True,
                    "category": route_info["category"],
                    "routed_to": target_model,
                    "why": route_info["why"],
                    "savings": route_info["cost_vs_gpt4"],
                    "classify_overhead_ms": route_info["classify_time_ms"]
                }

            resp_bytes = json.dumps(resp_data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_bytes)))
            self.send_header("X-AICraft-Routed-To", target_model.encode("ascii", "ignore").decode())
            if route_info:
                self.send_header("X-AICraft-Category", route_info["category"].encode("ascii", "ignore").decode())
                self.send_header("X-AICraft-Savings", route_info["cost_vs_gpt4"].encode("ascii", "ignore").decode())
            self.end_headers()
            self.wfile.write(resp_bytes)
        except Exception as e:
            self.send_error(502, str(e))

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok","router":"aicraft-auto"}')
        elif self.path == "/routes":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "classifier_model": CLASSIFIER_MODEL,
                "classifier_cost_per_call": "$0.0000006",
                "routes": {k: {"model": v["model"], "why": v["why"], "savings": v["cost_vs_gpt4"]} for k, v in ROUTE_MAP.items()}
            }, ensure_ascii=False).encode())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        print(f"[Router] {args[0]}")


def main():
    port = 3001
    server = HTTPServer(("0.0.0.0", port), RouterHandler)
    print(f"[Router] AICraft Auto Router 启动 :{port}")
    print(f"[Router] 分类器: {CLASSIFIER_MODEL} | 路由表: {len(ROUTE_MAP)} 条规则")
    server.serve_forever()


if __name__ == "__main__":
    main()
