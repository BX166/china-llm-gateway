"""Add history-based preference learning to Router v3"""

with open("/opt/aicraft/router/router.py", "r") as f:
    code = f.read()

# Add history tracking to learn_preference
old_learn = "def learn_preference(user_id, user_model, auto_model):"
new_learn = '''def get_preferred_from_history(user_id):
    """如果用户某个模型使用超70%,返回该模型"""
    pref = get_user_pref(user_id)
    hist = pref.get("routing_history", {})
    total = pref.get("total_routed", 0)
    if total >= 10:
        for model, count in hist.items():
            if count / total > 0.7:
                return model
    return None

def learn_preference(user_id, user_model, auto_model):'''
code = code.replace(old_learn, new_learn)

# Enhance learn_preference to track history
old_body = 'save_user_pref(user_id, pref)'
new_body = '''    # Track routing history for pattern learning
    if auto_model and user_id and user_id != "?":
        hist = pref.get("routing_history", {})
        hist[auto_model] = hist.get(auto_model, 0) + 1
        pref["routing_history"] = hist
        pref["total_routed"] = pref.get("total_routed", 0) + 1
    save_user_pref(user_id, pref)'''
code = code.replace(old_body, new_body)

# Add history check in route() before auto routing
old_check = '# 查用户偏好'
new_check = '''# 查用户偏好
    pref = get_user_pref(user_id) if user_id else {}

    # 历史学习：70%+请求走同一个模型 → 记住它
    hist_model = get_preferred_from_history(user_id)
    if hist_model:
        return hist_model, {"mode": "learned", "why": f"Based on your {pref.get('total_routed',0)} requests, using {hist_model}"}

    # 手动覆盖：3次以上 → 偏好'''
code = code.replace(old_check, new_check)

with open("/opt/aicraft/router/router.py", "w") as f:
    f.write(code)

print("History-based preference learning added")
