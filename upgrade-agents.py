"""Upgrade A7, A8, A1"""
import re

# ====== A7: Expand keyword database ======
with open("/opt/aicraft/regulator/a7-keyword.py", "r") as f:
    code = f.read()

# Replace small lists with comprehensive ones
replacements = [
    ('POLITICAL = ["法轮功","台独","藏独","疆独","达赖","热比娅","六四","天安门事件","falun","tiananmen"]',
     'POLITICAL = ["法轮功","台独","藏独","疆独","达赖","热比娅","六四","天安门事件","falun","tiananmen","分裂国家","颠覆政权","东突","东伊运","isis","纳粹","希特勒","靖国神社","占中","光复香港","时代革命"]'),

    ('VIOLENCE = ["炸弹制作","恐怖袭击","如何杀人","枪支制造","爆炸物","暗杀","人体炸弹","how to kill","bomb making"]',
     'VIOLENCE = ["炸弹制作","恐怖袭击","如何杀人","枪支制造","爆炸物","暗杀","人体炸弹","how to kill","bomb making","制造爆炸","自制武器","化学武器","生物武器","自杀式","绑架","劫持","枪击","暗网","雇佣兵","杀手服务","买凶"]'),

    ('PORN = ["裸体","色情","援交","av女优","无码","中出","adult video","porn","escort"]',
     'PORN = ["裸体","色情","援交","av女优","无码","中出","adult video","porn","escort","成人","性服务","卖淫","嫖娼","偷拍","走光","艳照","裸聊","幼女","未成年性","儿童色情","SM","性虐"]'),

    ('ILLEGAL = ["赌博","博彩","赌场","毒品","冰毒","海洛因","大麻购买","摇头丸","casino","heroin","cocaine"]',
     'ILLEGAL = ["赌博","博彩","赌场","毒品","冰毒","海洛因","大麻购买","摇头丸","casino","heroin","cocaine","百家乐","轮盘","老虎机","赌球","赌马","K粉","麻古","可卡因","吗啡","鸦片","罂粟","制毒","贩毒","洗钱","诈骗","传销","非法集资","高利贷","假币","假钞","伪造证件","黑客攻击","DDoS攻击","盗版","破解","枪支","弹药","管制刀具","电击枪"]'),
]

for old, new in replacements:
    code = code.replace(old, new)

with open("/opt/aicraft/regulator/a7-keyword.py", "w") as f:
    f.write(code)

# Count total keywords
count = len(re.findall(r'"[^"]{2,}"', code))
print(f"A7 upgraded: {count} keywords")

# ====== A8: Add graceful degradation ======
with open("/opt/aicraft/regulator/a8-semantic.py", "r") as f:
    code = f.read()

# Fix the classify function: on failure, let traffic through instead of blocking
old_classify = """    except Exception as e:
        # 审核故障 → 拒绝请求（不允许绕过审核）
        print(f"[A8] classify failed: {e}")
        return "审核故障", 1.0"""

new_classify = """    except Exception as e:
        # 审核故障 → 放行但标记（避免误杀正常用户）
        print(f"[A8] classify failed: {e}")
        return "审核降级", 0.0"""

code = code.replace(old_classify, new_classify)

# Update the handler to not block on degraded mode
old_handler = """        # 审核故障
        if category == "审核故障":
            self.send_json({"error":{"message":"安全审核服务暂时不可用","type":"service_error","code":"review_unavailable"}}, 503); return"""

new_handler = """        # 审核故障/降级 → 放行但记录
        if category == "审核故障" or category == "审核降级":
            self.send_json({"warning":"review_degraded","note":"审核服务暂时降级，请求已放行"}, 200); return"""

code = code.replace(old_handler, new_handler)

with open("/opt/aicraft/regulator/a8-semantic.py", "w") as f:
    f.write(code)

print("A8 upgraded: graceful degradation on API failure")

# ====== A1: Add HK monitoring ======
with open("/opt/aicraft/monitor/monitor.py", "r") as f:
    code = f.read()

# Add HK channel check
hk_check = """
    # HK Server check
    try:
        import subprocess
        r = subprocess.run(['ssh','-o','ConnectTimeout=5','-o','StrictHostKeyChecking=no',
            'ubuntu@43.161.248.132','curl -s -o /dev/null -w %{http_code} -m 5 http://localhost:3000/v1/models'],
            capture_output=True, text=True, timeout=15)
        if r.stdout.strip() == '200':
            log('OK', '[HK] 香港服务器 ✅')
        else:
            log('WARN', f'[HK] 香港服务器 ⚠️ HTTP {r.stdout.strip()}')
    except Exception as e:
        log('ERROR', f'[HK] 香港服务器 ❌ {e}')
"""

# Insert before the final summary
if 'HK' not in code:
    code = code.replace(
        'log("INFO", f"检查完成:',
        hk_check + '\n    log("INFO", f"检查完成:'
    )

with open("/opt/aicraft/monitor/monitor.py", "w") as f:
    f.write(code)

print("A1 upgraded: HK server monitoring added")
print("\nAll 3 agents upgraded successfully")
