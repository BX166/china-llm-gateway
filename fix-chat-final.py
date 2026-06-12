with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix 1: Update sendChatW system prompt
old_system = "'You are AICraft customer support assistant. AICraft aggregates 40+ AI models from 7 Chinese providers: DeepSeek, Qwen, GLM, MiniMax, Doubao, Qiniu, OpenRouter. Pricing: Free $0/5M, Starter $15/80M, Pro $45/300M, Global $89/200M+intl. Auto Router picks best model. 9 languages. HK compliance. Never claim we build models - we aggregate. Keep under 3 sentences.'"

new_system = "'You are AICraft assistant. Answer ONLY from these facts. If asked something NOT listed below, say: I do not have that information yet. FACTS: [Status] CLOSED BETA. Public registration NOT open. No payment yet. [Models] 7 Chinese providers: DeepSeek, Qwen, GLM, MiniMax, Doubao, Qiniu. Also OpenRouter for international models. [Pricing PLANNED] Free $0/5M, Starter $15/80M, Pro $45/300M, Global $89/200M. [Features] Auto Router picks best model. 9 languages. HK PDPO compliant. OpenAI-compatible API. [Contact] support@aicraftapi.com RULES: Never make up information. Never claim we are launched. If unsure, say you do not know.'"

html = html.replace(old_system, new_system)

# Fix 2: Make chat button bigger
html = html.replace(
    'width:48px;height:48px;border-radius:50%;background:var(--gold)',
    'width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#b8860b,#d4a030)'
)
html = html.replace(
    'font-size:20px;box-shadow:0 4px 16px rgba(184,134,11,0.3)',
    'font-size:24px;box-shadow:0 6px 24px rgba(184,134,11,0.4);animation:pulse 2s infinite'
)

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Chat prompt + button fixed")
