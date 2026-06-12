import re

with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# === COMPLETELY REWRITE LANGUAGE PICKER ===

# 1. Replace the lang trigger button to use simple href="#lang" onclick
old_btn = '<button class="lang-trigger" id="lt" onclick="toggleLang(event)"><span id="lf">EN</span> &#9662;</button>'
new_btn = '<button class="lang-trigger" id="lt" onclick="document.getElementById(\'lp\').classList.toggle(\'active\');return false;"><span id="lf">EN</span> &#9662;</button>'
if old_btn in html:
    html = html.replace(old_btn, new_btn)
else:
    # Try the other variant
    html = html.replace(
        '<button class="lang-trigger" id="lt"><span id="lf">EN</span> ▾</button>',
        '<button class="lang-trigger" id="lt" onclick="document.getElementById(\'lp\').classList.toggle(\'active\');return false;"><span id="lf">EN</span> ▾</button>'
    )

# 2. Add click-outside handler inline to the lang-picker div
old_picker = '<div class="lang-picker" id="lp">'
new_picker = '<div class="lang-picker" id="lp" onclick="event.stopPropagation()">'
html = html.replace(old_picker, new_picker)

# 3. Add a simple document click handler that closes the dropdown
# Find the </script> before </body>
close_drop_js = """
<script>
document.addEventListener('click',function(){document.getElementById('lp').classList.remove('active')});
</script>
"""
html = html.replace("</body>", close_drop_js + "\n</body>")

# 4. Remove any broken toggleLang references
html = html.replace("function toggleLang(e){e.preventDefault();e.stopPropagation();document.getElementById('lp').classList.toggle('active')}", "")
html = html.replace("document.addEventListener('click',function(e){var lp=document.getElementById('lp');if(lp&&!lp.contains(e.target))lp.classList.remove('active')});", "")

# 5. Make sure the language dropdown links have onclick that calls setLang
# Find lang-drop links and ensure they have proper onclick
# The existing JS creates lang-drop links dynamically. Let's make them static instead.

# Find the lang-drop div
old_drop = '<div class="lang-drop" id="ld"></div>'
static_drop = '<div class="lang-drop" id="ld">\n'
langs = [
    ('en', 'EN', 'English'),
    ('zh', '中文', '中文'),
    ('ja', '日本', '日本語'),
    ('ko', '한국', '한국어'),
    ('th', 'ไทย', 'ไทย'),
    ('id', 'ID', 'Bahasa Indonesia'),
    ('vi', 'VI', 'Tiếng Việt'),
    ('es', 'ES', 'Español'),
    ('pt', 'PT', 'Português'),
]
for code, flag, name in langs:
    static_drop += f'  <a href="#" onclick="setLang(\'{code}\');document.getElementById(\'lp\').classList.remove(\'active\');return false;">{flag} {name}</a>\n'
static_drop += '</div>'

html = html.replace(old_drop, static_drop)

# 6. Remove the dynamic language list builder from JS
# Find and remove: "var drop=document.getElementById(\"ld\");...langs.forEach..."
# We need to remove the code that builds the dropdown dynamically
# But keep the setLang function

html = re.sub(
    r'var drop=document\.getElementById\("ld"\)[^;]*;.*?appendChild\(a\)\}\);',
    '// Static lang list used instead\n',
    html,
    flags=re.DOTALL
)

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Language picker completely rebuilt with static HTML + inline onclick")
print("Static language links: 9")
