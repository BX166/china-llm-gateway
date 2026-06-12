with open("/opt/aicraft/web/index.html", "r") as f:
    html = f.read()

# English - remove direct competitor mentions
replacements = [
    ("OpenRouter doesn't have it. SiliconFlow doesn't have it. Qiniu doesn't have it. Only AICraft automatically selects the optimal model for every request.",
     "No other API platform offers automatic model selection. AICraft intelligently routes each request to the best model, saving up to 93% compared to always using GPT-4."),

    ("OpenRouter doesn't have it. SiliconFlow doesn't have it. Qiniu doesn't have it. Only AICraft automatically selects the optimal model for every request.",
     "No other API platform offers automatic model selection. AICraft intelligently routes each request to the best model, saving up to 93% compared to always using GPT-4."),

    # Chinese
    ("OpenRouter没有。硅基流动没有。七牛云没有。只有AICraft自动为每个请求选择最优模型。",
     "全球唯一提供Auto智能路由的API平台。AICraft自动为每个请求选择最优模型，相较全用GPT-4最高节省93%。"),
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        print(f"Fixed: {old[:40]}...")

with open("/opt/aicraft/web/index.html", "w") as f:
    f.write(html)

print("Done")
