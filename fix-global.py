with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix HTML element (the text shown before JS loads)
html = html.replace(
    'data-i18n="price_global_tokens">300M · Chinese + Intl<',
    'data-i18n="price_global_tokens">200M Chinese + Intl pay-per-use<'
)
html = html.replace(
    'data-i18n="price_global_f2">100M international models<',
    'data-i18n="price_global_f2">Intl models: cost + 25%<'
)

# 2. Fix all i18n JS strings for price_global_f2 (every language)
import re

# price_global_f2
old_f2 = re.findall(r'T\.(\w+)\["price_global_f2"\]="([^"]*)"', html)
zh_f2 = "国际模型: 成本+25%"
en_f2 = "Intl models: cost + 25%"
for lang, val in old_f2:
    old_line = f'T.{lang}["price_global_f2"]="{val}"'
    new_val = zh_f2 if lang == "zh" else en_f2
    new_line = f'T.{lang}["price_global_f2"]="{new_val}"'
    html = html.replace(old_line, new_line)
    print(f"Fixed f2: {lang}")

# price_global_tokens
old_tok = re.findall(r'T\.(\w+)\["price_global_tokens"\]="([^"]*)"', html)
zh_tok = "2亿国产 + 国际按量"
en_tok = "200M Chinese + Intl pay-per-use"
for lang, val in old_tok:
    old_line = f'T.{lang}["price_global_tokens"]="{val}"'
    new_val = zh_tok if lang == "zh" else en_tok
    new_line = f'T.{lang}["price_global_tokens"]="{new_val}"'
    html = html.replace(old_line, new_line)
    print(f"Fixed tok: {lang}")

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done - both HTML and all i18n fixed")
