#!/usr/bin/env python3
"""Add language picker to AICraft v3"""

with open("/opt/aicraft/web/index.html", "r") as f:
    html = f.read()

# 1. Add lang CSS before footer section
html = html.replace(
    "/* ========== FOOTER ========== */",
    """/* ========== LANG PICKER ========== */
.lang-picker{position:relative;margin-right:8px}
.lang-trigger{display:flex;align-items:center;gap:4px;background:var(--surface);border:1.5px solid var(--border);padding:6px 10px;border-radius:20px;font-size:12px;cursor:pointer;color:var(--text);white-space:nowrap}
.lang-trigger:hover{border-color:var(--gold)}
.lang-drop{display:none;position:absolute;top:100%;right:0;margin-top:4px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);min-width:150px;max-height:280px;overflow-y:auto;z-index:50;box-shadow:var(--shadow-lg)}
.lang-picker.active .lang-drop{display:block}
.lang-drop a{display:flex;align-items:center;gap:6px;padding:8px 14px;color:var(--text2);text-decoration:none;font-size:11px;transition:all 0.1s}
.lang-drop a:hover,.lang-drop a.sel{background:var(--gold-light);color:var(--gold);font-weight:600}

/* ========== FOOTER ========== */"""
)

# 2. Add lang picker HTML in nav
old = '<button class="nav-cta" onclick="openSignup()">Sign Up</button>'
new = '<div class="lang-picker" id="lang-picker"><button class="lang-trigger" id="lang-trigger"><span id="lang-flag">EN</span> &#9662;</button><div class="lang-drop" id="lang-drop"></div></div>\n    <button class="nav-cta" onclick="openSignup()">Sign Up</button>'
html = html.replace(old, new)

# 3. Add i18n data attributes to key elements
hero_title = '<h1>One API for <em>every frontier model</em></h1>'
html = html.replace(hero_title, '<h1><span data-i18n="hero_title_p1">One API for</span> <em><span data-i18n="hero_title_p2">every frontier model</span></em></h1>')

hero_desc = '<p>Access DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter & more through a single endpoint. Our Auto Router picks the best model for every task — saving up to 93% vs GPT-4.</p>'
html = html.replace(hero_desc, '<p data-i18n="hero_desc">Access DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter &amp; more through a single endpoint. Our Auto Router picks the best model for every task — saving up to 93% vs GPT-4.</p>')

# 4. Add lang JS before </body>
lang_js = """
<script>
// Language switcher
var langs=[{code:"en",name:"English",flag:"EN"},{code:"zh",name:"中文",flag:"中文"},{code:"ja",name:"日本語",flag:"日本"},{code:"ko",name:"한국어",flag:"한국"},{code:"th",name:"ไทย",flag:"ไท"},{code:"id",name:"Bahasa",flag:"ID"},{code:"vi",name:"Tieng Viet",flag:"VI"},{code:"es",name:"Espanol",flag:"ES"},{code:"pt",name:"Portugues",flag:"PT"}];
var i18n={en:{hero_title_p1:"One API for",hero_title_p2:"every frontier model",hero_badge:"7 Providers \\u00b7 40+ Models \\u00b7 Live",hero_desc:"Access DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter &amp; more through a single endpoint. Our Auto Router picks the best model for every task \\u2014 saving up to 93% vs GPT-4.",hero_cta1:"View Plans",hero_cta2:"API Docs",hero_cta3:"Create Free Account"},zh:{hero_title_p1:"一个API",hero_title_p2:"调用所有顶级模型",hero_badge:"7大渠道 \\u00b7 40+模型 \\u00b7 运行中",hero_desc:"通过统一端点访问DeepSeek、Qwen、GLM、MiniMax、Doubao、OpenRouter等40+模型。Auto智能路由器自动为每项任务选择最优模型\\u2014\\u2014相较GPT-4最高省省93%25。",hero_cta1:"查看方案",hero_cta2:"API文档",hero_cta3:"免费注册"}};
var drop=document.getElementById("lang-drop");
langs.forEach(function(l){var a=document.createElement("a");a.href="#";a.textContent=l.flag+" "+l.name;a.onclick=function(e){e.preventDefault();setLang(l.code)};drop.appendChild(a)});
document.getElementById("lang-trigger").onclick=function(e){e.preventDefault();e.stopPropagation();document.getElementById("lang-picker").classList.toggle("active")};
document.addEventListener("click",function(e){if(!document.getElementById("lang-picker").contains(e.target))document.getElementById("lang-picker").classList.remove("active")});
function setLang(code){var l=langs.find(function(x){return x.code===code})||langs[0];document.getElementById("lang-flag").textContent=l.flag;localStorage.setItem("aicraft-lang",code);var d=i18n[code]||i18n.en;document.querySelectorAll("[data-i18n]").forEach(function(el){if(d[el.dataset.i18n])el.textContent=d[el.dataset.i18n]});document.querySelectorAll(".lang-drop a").forEach(function(a){a.classList.remove("sel");if(a.textContent.includes(l.name))a.classList.add("sel")})}
setLang(localStorage.getItem("aicraft-lang")||"en");
</script>
"""
html = html.replace("</body>", lang_js + "\n</body>")

with open("/opt/aicraft/web/index.html", "w") as f:
    f.write(html)

print("Language picker added OK")
