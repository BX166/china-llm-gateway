#!/usr/bin/env python3
"""AICraft A9 - 多模态文件扫描 Agent · :3013"""

import json, os, re, hashlib, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path

PORT = 3013
LOG_DIR = Path("/opt/aicraft/regulator/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
SCAN_LOG = LOG_DIR / "a9_scan_log.jsonl"

# 禁止的文件类型
BLOCKED_EXTENSIONS = {".exe", ".bat", ".sh", ".ps1", ".vbs", ".scr", ".dll", ".sys"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_NESTED_DEPTH = 3  # 压缩包嵌套深度

# 图片检测规则（简单启发式）
IMAGE_SIGNATURES = {
    b"\x89PNG": ".png",
    b"\xff\xd8\xff": ".jpg",
    b"GIF87a": ".gif",
    b"GIF89a": ".gif",
    b"RIFF": ".webp",
}


def log_scan(user_id, ip, filename, result, detail):
    entry = {"time": datetime.now().isoformat(), "user_id": user_id, "ip": ip,
             "filename": filename, "result": result, "detail": detail[:200]}
    with open(SCAN_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def check_file(data, filename):
    """检测文件安全性"""
    if not data or not filename:
        return "blocked", "empty file"

    # 1. 大小检查
    if len(data) > MAX_FILE_SIZE:
        return "blocked", f"file too large: {len(data)} bytes"

    # 2. 扩展名黑名单
    ext = Path(filename).suffix.lower()
    if ext in BLOCKED_EXTENSIONS:
        return "blocked", f"forbidden extension: {ext}"

    # 3. 文件头魔数校验（防止伪造扩展名）
    for magic, real_ext in IMAGE_SIGNATURES.items():
        if data[:len(magic)] == magic:
            if ext not in (real_ext, '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'):
                return "blocked", f"extension mismatch: {ext} vs {real_ext}"

    # 4. 文本文件内容扫描
    if ext in {".txt", ".md", ".csv", ".json", ".xml", ".yml", ".yaml", ".ini", ".cfg", ".log"}:
        try:
            text = data.decode("utf-8", errors="ignore")[:5000]
            # 检测脚本注入
            patterns = [
                (r'<script[^>]*>', 'script tag'),
                (r'eval\s*\(', 'eval() call'),
                (r'exec\s*\(', 'exec() call'),
                (r'__import__\s*\(', 'import() call'),
                (r'os\.system\s*\(', 'system() call'),
                (r'subprocess\.', 'subprocess'),
            ]
            for pat, name in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    return "blocked", f"code injection: {name}"
        except Exception:
            pass

    return "passed", f"clean: {ext}"


class A9Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/scan":
            cl = int(self.headers.get("Content-Length", 0))
            if cl == 0 or cl > MAX_FILE_SIZE:
                self.send_json({"result": "blocked", "reason": "invalid size"}, 400)
                return

            body = self.rfile.read(cl)
            filename = self.headers.get("X-Filename", "unknown")
            user_id = self.headers.get("X-User-ID", "?")
            user_ip = self.headers.get("X-Real-IP", self.client_address[0])

            result, detail = check_file(body, filename)
            log_scan(user_id, user_ip, filename, result, detail)

            if result == "blocked":
                self.send_json({"result": result, "reason": detail}, 400)
            else:
                self.send_json({"result": result, "detail": detail}, 200)
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == "/health":
            self.send_json({"status": "ok", "agent": "A9", "blocked_exts": len(BLOCKED_EXTENSIONS)}, 200)
        else:
            self.send_error(404)

    def send_json(self, data, code):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, fmt, *args): pass


def main():
    print(f"[A9] File Scanner :{PORT} | blocked: {len(BLOCKED_EXTENSIONS)} exts | max: {MAX_FILE_SIZE//1024//1024}MB")
    HTTPServer(("0.0.0.0", PORT), A9Handler).serve_forever()


if __name__ == "__main__":
    main()
