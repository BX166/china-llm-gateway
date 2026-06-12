with open("/opt/aicraft/web/index.html", "r") as f:
    html = f.read()

# Fix: Add inline onclick to lang trigger button
old_btn = '<button class="lang-trigger" id="lt">'
new_btn = '<button class="lang-trigger" id="lt" onclick="toggleLang(event)">'
html = html.replace(old_btn, new_btn)

# Fix: Add toggleLang function before setLang
js_fix = """
function toggleLang(e){e.preventDefault();e.stopPropagation();document.getElementById('lp').classList.toggle('active')}
document.addEventListener('click',function(e){var lp=document.getElementById('lp');if(lp&&!lp.contains(e.target))lp.classList.remove('active')});
"""
html = html.replace("function setLang(c){", js_fix + "function setLang(c){")

with open("/opt/aicraft/web/index.html", "w") as f:
    f.write(html)

print("Language picker fixed")
