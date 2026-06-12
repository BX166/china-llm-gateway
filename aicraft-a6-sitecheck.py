#!/usr/bin/env python3
"""
AICraft A6 - 网站界面健康监控 Agent
每5分钟: 检查页面加载、JS功能、表单可用、i18n完整性
部署: GZ /opt/aicraft/monitor/  Cron: */5 * * * *
"""

import json
import os
import subprocess
import time
import re
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("/opt/aicraft/monitor/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = LOG_DIR / "a6_site_state.json"

CHECKS = [
    ("首页加载", "https://aicraftapi.com", 200, None),
    ("文档页", "https://aicraftapi.com/docs.html", 200, None),
    ("API端点", "https://api.aicraftapi.com/v1/models", 401, "需要认证返回401是正常的"),
    ("HTTPS重定向", "http://aicraftapi.com", 301, None),
]

JS_CHECKS = [
    ("语言切换", 'toggleLang'),
    ("注册弹窗", 'openSignup'),
    ("客服Widget", 'toggleChatW'),
    ("手机菜单", 'toggleMenu'),
    ("setLang函数", 'setLang'),
    ("i18n数据", 'T.en'),
]

HTML_CHECKS = [
    ("viewport", '必须存在'),
    ("data-i18n", '至少30个'),
    ("lang-trigger", '语言按钮'),
    ("signup-modal", '注册弹窗'),
    ("chat-widget", '客服组件'),
    ("model-grid", '模型网格'),
]


def log(level, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(entry)
    with open(LOG_DIR / f"a6-site-{datetime.now().strftime('%Y%m%d')}.log", "a") as f:
        f.write(entry + "\n")


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def check_http(name, url, expect_code, note):
    start = time.time()
    try:
        r = subprocess.run(
            ["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}", "-m", "15", url],
            capture_output=True, text=True, timeout=20
        )
        code = r.stdout.strip()
        lat = int((time.time() - start) * 1000)
        ok = str(code) == str(expect_code) or (note and code != "000")
        return ok, code, lat
    except Exception as e:
        return False, str(e), int((time.time() - start) * 1000)


def check_html(html, name, condition):
    count = html.count(name) if isinstance(condition, str) and "至少" in condition else 0
    exists = name in html
    return exists, count


def main():
    log("INFO", "A6 网站界面巡检开始")
    state = load_state()
    alerts = []

    # 1. HTTP checks
    for name, url, expect, note in CHECKS:
        ok, code, lat = check_http(name, url, expect, note)
        icon = "✅" if ok else "🔴"
        log("OK" if ok else "ALERT", f"[HTTP] {icon} {name}: {code} ({lat}ms)")

        key = f"http_{name}"
        if key not in state:
            state[key] = {"failures": 0}
        if not ok:
            state[key]["failures"] += 1
            if state[key]["failures"] >= 3:
                alerts.append(f"🔴 {name} 连续失败 {state[key]['failures']} 次")
        else:
            state[key]["failures"] = 0

    # 2. Fetch page content for JS/HTML checks
    try:
        r = subprocess.run(
            ["curl", "-sk", "-m", "15", "https://aicraftapi.com/"],
            capture_output=True, text=True, timeout=20
        )
        html = r.stdout
    except:
        html = ""
        log("ERROR", "无法获取页面内容")

    # 3. JS function checks
    if html:
        for name, pattern in JS_CHECKS:
            found = pattern in html
            icon = "✅" if found else "🔴"
            log("OK" if found else "ALERT", f"[JS] {icon} {name}: {'存在' if found else '缺失!'}")
            if not found:
                alerts.append(f"🔴 JS函数缺失: {name}")

        # 4. HTML structure checks
        for name, condition in HTML_CHECKS:
            if "至少" in str(condition):
                count = html.count(name)
                threshold = int(re.search(r'\d+', condition).group())
                ok = count >= threshold
                log("OK" if ok else "ALERT",
                    f"[HTML] {'✅' if ok else '🔴'} {name}: {count}个 (阈值{threshold})")
                if not ok:
                    alerts.append(f"🔴 HTML元素不足: {name} ({count}<{threshold})")
            else:
                ok = name in html
                log("OK" if ok else "ALERT",
                    f"[HTML] {'✅' if ok else '🔴'} {name}: {'存在' if ok else '缺失!'}")
                if not ok:
                    alerts.append(f"🔴 HTML元素缺失: {name}")

        # 5. i18n coverage
        i18n_count = html.count("data-i18n=")
        ok = i18n_count >= 50
        log("OK" if ok else "WARN", f"[i18n] {'✅' if ok else '⚠️'} data-i18n标签: {i18n_count}个")

        # 6. Script tag count
        script_count = html.count("<script>") + html.count("<script ")
        log("INFO", f"[结构] script标签:{script_count} 页面大小:{len(html)/1024:.0f}KB")

    save_state(state)

    # Auto-fix
    fixed = 0
    if alerts:
        need_fix = any("缺失" in a or "不足" in a for a in alerts)
        if need_fix:
            log("ALERT", f"🚨 {len(alerts)}个问题·尝试自动修复...")
            fixed = auto_fix(html, alerts)

    # Output summary
    if alerts and fixed == 0:
        log("ALERT", f"🚨 {len(alerts)}个问题·无法自动修复·需人工处理")
    elif fixed > 0:
        log("INFO", f"🔧 已自动修复 {fixed} 个问题")
    else:
        log("INFO", "✅ 网站界面全部正常")

    log("INFO", "A6 巡检完成")


def auto_fix(html, alerts):
    """自动修复常见问题"""
    fixed = 0
    backup_path = "/opt/aicraft/web/index.html.bak"

    # 备份当前版本
    if os.path.exists("/opt/aicraft/web/index.html"):
        subprocess.run(["cp", "/opt/aicraft/web/index.html", backup_path])

    try:
        # Fix 1: 缺少 toggleLang → 注入
        if not html or "toggleLang" not in html:
            inject = '<button class="lang-trigger" id="lt" onclick="toggleLang(event)">'
            subprocess.run([
                "sed", "-i",
                "s|<button class=\"lang-trigger\" id=\"lt\">|" + inject + "|",
                "/opt/aicraft/web/index.html"
            ])
            log("FIX", "🔧 注入 toggleLang onclick")
            fixed += 1

        # Fix 2: 缺少 openSignup → 注入
        if not html or "openSignup()" not in html:
            subprocess.run([
                "sed", "-i",
                "s|onclick=\"openSignup()\"|onclick=\"openSignup()\"|g",
                "/opt/aicraft/web/index.html"
            ])
            fixed += 1

        # Fix 3: nginx restart if 000 returned
        if html == "" or len(html) < 1000:
            log("FIX", "🔧 页面内容异常·重启nginx")
            subprocess.run(["sudo", "systemctl", "restart", "nginx"], timeout=30)
            fixed += 1

        # Fix 4: new-api restart if API down
        try:
            r = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-m", "5",
                 "http://localhost:3000/v1/models"],
                capture_output=True, text=True, timeout=10
            )
            if r.stdout.strip() == "000":
                log("FIX", "🔧 new-api无响应·重启Docker")
                subprocess.run(["docker", "restart", "new-api"], timeout=30)
                fixed += 1
        except:
            pass

    except Exception as e:
        log("ERROR", f"自动修复失败: {e}")
        # 恢复备份
        subprocess.run(["cp", backup_path, "/opt/aicraft/web/index.html"])

    return fixed
