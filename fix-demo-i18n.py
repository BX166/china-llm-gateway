with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix 1: dark mode particle opacity
html = html.replace(
    "body.dark .par div { opacity: 0.05; }",
    "body.dark .par div { opacity: 0.08; }"
)

# Fix 2: add data-i18n to demo title
html = html.replace(
    '<h2 style="font-size:26px;font-weight:800;margin-bottom:8px">3 lines of code.<br>40+ models at your fingertips.</h2>',
    '<h2 style="font-size:26px;font-weight:800;margin-bottom:8px" data-i18n="demo_title">3 lines of code.<br>40+ models at your fingertips.</h2>'
)

# Fix 3: add data-i18n to demo description
html = html.replace(
    '<p style="color:#6b7280;font-size:15px;line-height:1.7;margin-bottom:16px">Drop-in replacement for OpenAI. Auto Router picks the best model for every task',
    '<p style="color:#6b7280;font-size:15px;line-height:1.7;margin-bottom:16px" data-i18n="demo_desc">Drop-in replacement for OpenAI. Auto Router picks the best model for every task'
)

# Fix 4: add i18n translations for demo section
i18n_block = """
T.en["demo_title"]="3 lines of code.<br>40+ models at your fingertips.";
T.zh["demo_title"]="三行代码。<br>40+模型触手可及。";
T.ja["demo_title"]="3行のコード。<br>40以上のモデルが指先に。";
T.pt["demo_title"]="3 linhas de codigo.<br>40+ modelos ao seu alcance.";
T.es["demo_title"]="3 lineas de codigo.<br>40+ modelos a tu alcance.";
T.en["demo_desc"]="Drop-in replacement for OpenAI. Auto Router picks the best model for every task. No more manual switching. No more overpaying.";
T.zh["demo_desc"]="OpenAI直接替换。Auto Router自动选最优模型。无需手动切换。不再多花冤枉钱。";
T.ja["demo_desc"]="OpenAIの代替。Auto Routerが最適なモデルを自動選択。手動切替不要。";
T.pt["demo_desc"]="Substituto direto do OpenAI. Auto Router escolhe o melhor modelo. Sem troca manual.";
T.es["demo_desc"]="Reemplazo directo de OpenAI. Auto Router elige el mejor modelo. Sin cambios manuales.";
"""

html = html.replace(
    '\nfunction setLang(code) {',
    i18n_block + '\nfunction setLang(code) {'
)

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Fixed: dark mode particles + demo i18n + translations")
