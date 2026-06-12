#!/usr/bin/env python3
"""AICraft A6 - Site Health Monitor with Auto-Fix · Runs every 5 min"""

import os
import subprocess
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("/opt/aicraft/monitor/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = LOG_DIR / "a6_site_state.json"

def log(level, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(entry, flush=True)
    try:
        with open(LOG_DIR / f"a6-site-{datetime.now().strftime('%Y%m%d')}.log", "a") as f:
            f.write(entry + "\n")
    except Exception:
        pass

def fetch_page():
    try:
        r = subprocess.run(["curl", "-sk", "-m", "15", "https://aicraftapi.com/"],
                           capture_output=True, text=True, timeout=20)
        return r.stdout
    except Exception:
        return ""

def check_api():
    try:
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-m", "5",
                            "http://localhost:3000/v1/models"],
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except Exception:
        return "000"

def auto_fix(html):
    fixes = 0

    # 1. Check if HTML is valid
    if not html or len(html) < 1000:
        log("FIX", "Page empty - restarting nginx")
        subprocess.run(["sudo", "systemctl", "restart", "nginx"], timeout=30)
        return 1

    # 2. Check JS functions exist
    required_js = ["toggleLang", "openSignup", "toggleChatW", "setLang"]
    missing = [f for f in required_js if f not in html]
    if missing:
        log("FIX", "JS functions missing: " + ",".join(missing) + " - restoring from backup")
        if os.path.exists("/opt/aicraft/web/index.html.bak"):
            subprocess.run(["cp", "/opt/aicraft/web/index.html.bak", "/opt/aicraft/web/index.html"])
            fixes += 1

    # 3. Check API is up
    if check_api() == "000":
        log("FIX", "new-api down - restarting")
        subprocess.run(["docker", "restart", "new-api"], timeout=30)
        fixes += 1

    # 4. Check data-i18n
    i18n_count = html.count("data-i18n=")
    if i18n_count < 30:
        log("FIX", f"i18n tags only {i18n_count} - too few")
        if os.path.exists("/opt/aicraft/web/index.html.bak"):
            subprocess.run(["cp", "/opt/aicraft/web/index.html.bak", "/opt/aicraft/web/index.html"])
            fixes += 1

    return fixes

def main():
    log("INFO", "A6 site check starting")

    # Fetch page
    html = fetch_page()

    if not html:
        log("ALERT", "Cannot fetch page!")
        auto_fix("")
        return

    page_size = len(html)
    log("INFO", f"Page loaded: {page_size//1024}KB")

    # Check JS
    for fn in ["toggleLang", "openSignup", "closeSignup", "toggleChatW", "setLang", "toggleMenu"]:
        ok = fn in html
        log("OK" if ok else "ALERT", f"[JS] {fn}: {'OK' if ok else 'MISSING'}")

    # Check HTML
    for el, threshold in [("data-i18n=", 50), ("model-grid", 1), ("chat-widget", 1)]:
        count = html.count(el)
        ok = count >= threshold
        log("OK" if ok else "ALERT", f"[HTML] {el}: {count} (need {threshold})")

    # Check API
    api = check_api()
    log("OK" if api != "000" else "ALERT", f"[API] new-api: {api}")

    # Auto-fix if needed
    has_issues = any(f not in html for f in ["toggleLang", "openSignup", "setLang"])
    has_issues = has_issues or (html.count("data-i18n=") < 30) or (api == "000")

    if has_issues:
        log("ALERT", "Issues detected - running auto-fix")
        n = auto_fix(html)
        log("INFO", f"Auto-fix: {n} issues resolved")
    else:
        log("INFO", "All checks passed")

    # Backup if healthy
    if not has_issues and page_size > 50000:
        subprocess.run(["cp", "/opt/aicraft/web/index.html", "/opt/aicraft/web/index.html.bak"])

    log("INFO", "A6 completed")

if __name__ == "__main__":
    main()
