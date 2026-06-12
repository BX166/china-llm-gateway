with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Clearer wording
# EN
html = html.replace(
    'T.en["price_global_tokens"]="200M Chinese + Intl pay-per-use"',
    'T.en["price_global_tokens"]="200M tokens (Chinese models)"'
)
html = html.replace(
    'T.en["price_global_f2"]="Intl models: cost + 25%"',
    'T.en["price_global_f2"]="GPT-4o, Claude, Gemini — from $3.13/M"'
)
# ZH
html = html.replace(
    'T.zh["price_global_tokens"]="2亿国产 + 国际按量"',
    'T.zh["price_global_tokens"]="2亿Token（国产模型）"'
)
html = html.replace(
    'T.zh["price_global_f2"]="国际模型: 成本+25%"',
    'T.zh["price_global_f2"]="GPT-4o, Claude, Gemini — 低至 ¥22/M"'
)
# JA
html = html.replace(
    'T.ja["price_global_tokens"]="200M CN + Intl pay-per-use"',
    'T.ja["price_global_tokens"]="2億トークン（中国モデル）"'
)
# PT
html = html.replace(
    'T.pt["price_global_tokens"]="200M CN + Intl pay-per-use"',
    'T.pt["price_global_tokens"]="200M tokens (modelos chineses)"'
)
# ES
html = html.replace(
    'T.es["price_global_tokens"]="200M CN + Intl pay-per-use"',
    'T.es["price_global_tokens"]="200M tokens (modelos chinos)"'
)
# ID
html = html.replace(
    'T.id["price_global_tokens"]="200M CN + Intl pay-per-use"',
    'T.id["price_global_tokens"]="200M token (model China)"'
)

# Also fix HTML defaults
old_html_tok = 'data-i18n="price_global_tokens">200M Chinese + Intl pay-per-use<'
new_html_tok = 'data-i18n="price_global_tokens">200M tokens (Chinese models)<'
html = html.replace(old_html_tok, new_html_tok)

old_html_f2 = 'data-i18n="price_global_f2">Intl models: cost + 25%<'
new_html_f2 = 'data-i18n="price_global_f2">GPT-4o, Claude, Gemini — from $3.13/M<'
html = html.replace(old_html_f2, new_html_f2)

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
