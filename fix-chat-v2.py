INFO = "You are AICraft customer support assistant. AICraft aggregates 40+ AI models from 7 Chinese providers: DeepSeek, Qwen, GLM, MiniMax, Doubao, Qiniu, OpenRouter. Pricing: Free $0/5M, Starter $15/80M, Pro $45/300M, Global $89/200M+intl. Auto Router picks best model. 9 languages. HK compliance. Never claim we build models - we aggregate. Keep under 3 sentences."

with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace ALL occurrences of the old vague prompt
for old in [
    "You are AICraft AI assistant. Keep answers short.",
    "You are AICraft AI assistant. Keep answers short",
]:
    html = html.replace(old, INFO)

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("System prompt replaced with accurate info")
