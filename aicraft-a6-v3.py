#!/usr/bin/env python3
"""
AICraft A6 v3 — 全站交互检测 Agent
检测所有页面: 点击 · 弹窗 · 标签 · 翻译 · 暗色模式 · 渲染
部署: GZ /opt/aicraft/monitor/ · Cron: */5 * * * *
"""

import re
import subprocess
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("/opt/aicraft/monitor/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

PAGES_TO_CHECK = [
    ("首页", "https://aicraftapi.com/"),
    ("文档", "https://aicraftapi.com/docs.html"),
    ("状态", "https://aicraftapi.com/status.html"),
]

CHECKS = []

def check(name):
    """注册一个检测项"""
    def decorator(func):
        CHECKS.append((name, func))
        return func
    return decorator


# ====== 首页检测 ======

@check("首页: 模型标签可点击")
def test_model_tabs(html):
    """检测3个标签按钮和对应的面板"""
    tabs = html.count('tab-btn')
    panels = html.count('tab-panel')
    has_handler = 'forEach' in html and 'data-tab' in html
    return tabs >= 3 and panels >= 3 and has_handler, f"tabs:{tabs} panels:{panels} handler:{has_handler}"


@check("首页: 语言选择器")
def test_lang_switcher(html):
    """检测语言切换器元素完整"""
    trigger = 'lang-trigger' in html
    dropdown = 'lang-drop' in html
    setlang = 'function setLang' in html or 'setLang' in html
    langs = len(re.findall(r'T\.(en|zh|ja|ko|th|id|vi|es|pt)\[', html))
    return trigger and dropdown and setlang, f"trigger:{trigger} dropdown:{dropdown} fn:{setlang} langs:{langs}"


@check("首页: 注册弹窗")
def test_signup_modal(html):
    """检测注册弹窗打开/关闭函数"""
    open_fn = 'function openSignup' in html or 'openSignup()' in html
    close_fn = 'function closeSignup' in html or 'closeSignup()' in html
    modal = 'signup-modal' in html or 'id="sm"' in html
    return open_fn and close_fn and modal, f"open:{open_fn} close:{close_fn} modal:{modal}"


@check("首页: 客服Widget")
def test_chat_widget(html):
    """检测客服组件完整"""
    toggle = 'toggleChatW' in html
    send = 'sendChatW' in html
    panel = 'chat-panel' in html or 'id="cpw"' in html
    return toggle and send and panel, f"toggle:{toggle} send:{send} panel:{panel}"


@check("首页: 暗色模式")
def test_dark_mode(html):
    """检测暗色模式CSS覆盖"""
    dark_rules = len(re.findall(r'body\.dark\s', html))
    toggle_fn = 'toggleTheme' in html or 'classList.toggle.*dark' in html
    return dark_rules >= 10 and toggle_fn, f"dark_rules:{dark_rules} toggle:{toggle_fn}"


@check("首页: i18n翻译覆盖")
def test_i18n(html):
    """检测data-i18n标签都有翻译"""
    tags = len(re.findall(r'data-i18n="([^"]+)"', html))
    en_keys = len(re.findall(r'T\.en\["([^"]+)"\]', html))
    zh_keys = len(re.findall(r'T\.zh\["([^"]+)"\]', html))
    return en_keys >= tags * 0.9 and zh_keys >= tags * 0.9, f"tags:{tags} en:{en_keys} zh:{zh_keys}"


@check("首页: 模型数据渲染")
def test_model_data(html):
    """检测模型数据能被JS渲染"""
    has_tcm = 'var tcm=' in html or 'DeepSeek' in html
    has_grid = 'model-grid' in html or 'id="gtc"' in html
    return has_tcm and has_grid, f"data:{has_tcm} grid:{has_grid}"


@check("首页: 定价卡片")
def test_pricing_cards(html):
    """检测4档定价卡片存在"""
    cards = ['price_free', 'price_starter', 'price_pro', 'price_global']
    found = sum(1 for c in cards if c in html)
    return found >= 4, f"cards:{found}/4"


@check("首页: 导航链接")
def test_nav_links(html):
    """检测导航链接完整"""
    links = ['#models', '#pricing', '#router', '#docs', '#privacy']
    found = sum(1 for l in links if l in html)
    return found >= 4, f"links:{found}/5"


@check("文档页: 内容完整")
def test_docs_page(html):
    """检测文档页有关键内容"""
    return 'Quick Start' in html or '快速开始' in html or 'API' in html, "docs content"


@check("状态页: 渠道检测")
def test_status_page(html):
    """检测状态页有渠道信息"""
    return 'channel' in html.lower() or 'Channel' in html or '渠道' in html, "status content"


@check("监管看板: 可访问")
def test_regulator():
    """检测监管看板登录页可访问"""
    try:
        r = subprocess.run(["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}", "-m", "5",
                            "https://aicraftapi.com/regulator/login"],
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip() == "200", f"HTTP {r.stdout.strip()}"
    except:
        return False, "unreachable"


def fetch_page(url):
    try:
        r = subprocess.run(["curl", "-sk", "-m", "10", url],
                           capture_output=True, text=True, timeout=15)
        return r.stdout
    except:
        return ""


def log(level, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(entry, flush=True)
    logfile = LOG_DIR / f"a6-v3-{datetime.now().strftime('%Y%m%d')}.log"
    with open(logfile, "a") as f:
        f.write(entry + "\n")


def main():
    log("INFO", "A6 v3 全站交互检测开始")
    html_cache = {}

    # 先拉所有页面
    for name, url in PAGES_TO_CHECK:
        html = fetch_page(url)
        html_cache[name] = html
        ok = len(html) > 1000
        log("OK" if ok else "ALERT", f"页面加载: {name} ({len(html)} bytes)")

    # 跑所有检测
    passed = 0
    failed = 0
    for check_name, check_fn in CHECKS:
        # Determine which page this check applies to
        if "首页" in check_name:
            html = html_cache.get("首页", "")
        elif "文档" in check_name:
            html = html_cache.get("文档", "")
        elif "状态" in check_name:
            html = html_cache.get("状态", "")
        elif "监管" in check_name:
            html = ""  # Special check (curl)
        else:
            html = html_cache.get("首页", "")

        try:
            ok, detail = check_fn(html) if html else check_fn()
            tag = "OK" if ok else "ALERT"
            log(tag, f"{check_name}: {detail}")
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            log("ERROR", f"{check_name}: Exception - {e}")
            failed += 1

    # 自动修复
    if failed > 0:
        log("FIX", f"发现问题 {failed} 项，尝试从备份恢复")
        backup = Path("/opt/aicraft/web/index.html.bak")
        web = Path("/opt/aicraft/web/index.html")
        if backup.exists() and web.exists():
            web_bak = web.read_text()
            backup_size = len(backup.read_text())
            current_size = len(web_bak)
            if backup_size > 50000 and current_size < backup_size * 0.8:
                log("FIX", f"页面异常缩小({current_size}<>{backup_size})，恢复备份")
                subprocess.run(["cp", str(backup), str(web)])
                subprocess.run(["sudo", "systemctl", "reload", "nginx"])
                log("FIX", "已恢复备份并重载nginx")

    log("INFO", f"检测完成: {passed}/{passed+failed} 通过")


if __name__ == "__main__":
    main()
