
with open(r"c:\Users\Brian\xundao\hn-meeting-v3.html", "r", encoding="utf-8") as f:
    html = f.read()

# Only replace in content (not CSS tags or HTML structure)
# Target: English terms that government officials won't understand
replacements = [
    # API / Auth
    ("获取API Key", "获取API密钥"),
    ("Auto Router", "自动路由"),
    ("OpenAI 兼容格式", "开放接口兼容格式"),
    ("3 行代码接入", "三行代码接入"),

    # Pricing (keep $ amounts, translate plan names)
    ("Free $0", "免费 $0"),
    ("/ Starter $15", "/ 入门 $15"),
    ("/ Pro $45", "/ 专业 $45"),
    ("/ Global $89", "/ 全球 $89"),

    # Legal
    ("PDPO + SCCs", "香港私隐条例(PDPO) + 标准合同条款"),
    ("PDPO", "香港私隐条例"),
    ("SCCs", "标准合同条款"),
    ("APPI认可", "日本个人信息保护法认可"),
    ("LGPD认可", "巴西数据保护法认可"),

    # Tech
    ("Token数", "令牌数"),
    ("Token 检测", "令牌检测"),
    ("Agent 体系", "智能监管系统"),
    ("Agent 监管", "智能监管"),
    ("Agent", "监管代理"),
    ("3σ", "三倍正常波动"),

    # Security
    ("API 滥用", "接口滥用"),
    ("API调用", "接口调用"),

    # Fix PDPO double expansion
    ("香港私隐条例(香港私隐条例)", "香港私隐条例"),
    ("PDPO(香港私隐条例)", "PDPO(香港私隐条例)"),
]

for old, new in replacements:
    html = html.replace(old, new)

# Fix: HK server line
html = html.replace("香港私隐条例) → 实时转发国产模型", "PDPO) → 实时转发国产模型")
html = html.replace("香港私隐条例) → 海南路由", "PDPO) → 海南路由")

with open(r"c:\Users\Brian\xundao\hn-meeting-v3.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Replaced English terms with Chinese")
