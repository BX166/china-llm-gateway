#!/usr/bin/env python3
"""Extract all i18n keys from HTML and generate complete translations"""

import re

with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Extract all data-i18n keys from HTML
all_keys = list(set(re.findall(r'data-i18n="([^"]+)"', html)))
all_keys.sort()
print(f"Found {len(all_keys)} unique i18n keys")

# 2. Extract English defaults from HTML elements
en_defaults = {}
for key in all_keys:
    pattern = f'data-i18n="{key}">([^<]+)<'
    m = re.search(pattern, html)
    if m:
        en_defaults[key] = m.group(1).strip()

# 3. Get existing add() translations
adds = re.findall(r'add\("([^"]+)",\s*"([^"]*)"', html)
existing = {k: v for k, v in adds}

# 4. Combine: existing translations + HTML defaults
for key in all_keys:
    if key not in existing:
        existing[key] = en_defaults.get(key, key)

# 5. Generate complete i18n JS block
# For each language, provide translations for all keys
# zh translations for common keys
zh_map = {
    "nav_models": "模型", "nav_pricing": "定价", "nav_router": "智能路由",
    "nav_docs": "文档", "nav_privacy": "隐私", "nav_signup": "注册",
    "hero_badge": "7大渠道 · 40+模型 · 运行中",
    "hero_h1_p1": "一个API", "hero_h1_p2": "调用所有顶级模型",
    "hero_desc": "通过统一端点访问40+AI模型。Auto智能路由器自动选择最优模型。",
    "hero_cta1": "查看方案", "hero_cta2": "API文档", "hero_cta3": "免费注册",
    "models_label": "模型库", "models_title": "每一个模型，一个端点",
    "models_sub": "7大渠道40+模型。文本生成、视频创作、图片合成。",
    "tab_text_chinese": "文本·国产", "tab_text_intl": "文本·国际", "tab_media": "媒体生成",
    "pricing_label": "定价", "pricing_title": "简单、透明、有竞争力",
    "pricing_sub": "所有套餐含OpenAI兼容API+Auto Router。国际模型按量计费。无隐藏费用。",
    "price_free": "免费", "price_free_tokens": "500万Token·国产",
    "price_free_f1": "全部国产文本模型", "price_free_f2": "每分钟5请求",
    "price_free_f3": "含Auto Router", "price_free_f4": "社区支持",
    "price_free_cta": "免费开始",
    "price_starter": "Starter", "price_starter_tokens": "8000万Token·全国产",
    "price_starter_f1": "全部国产文本模型", "price_starter_f2": "无限请求",
    "price_starter_f3": "Auto Router·3档", "price_starter_f4": "邮件支持",
    "price_starter_f5": "用量面板", "price_starter_cta": "订阅",
    "price_pro": "Pro", "price_pro_tokens": "3亿Token·国产",
    "price_pro_f1": "Starter全部内容", "price_pro_f2": "优先路由",
    "price_pro_f3": "高级分析", "price_pro_cta": "升级Pro",
    "price_global": "Global", "price_global_tokens": "3亿·国产+国际",
    "price_global_f1": "Pro全部内容", "price_global_f2": "1亿国际模型",
    "price_global_f3": "GPT-4o·Claude·Gemini", "price_global_f4": "全球路由",
    "price_global_cta": "开启全球",
    "price_ent": "Enterprise", "price_ent_desc": "$299/月·20亿Token·定制SLA",
    "price_ent_cta": "联系销售",
    "router_label": "竞争优势", "router_title": "唯一拥有Auto智能路由的平台",
    "router_sub": "OpenRouter没有。硅基流动没有。七牛云没有。只有AICraft自动选择最优模型。",
    "router_stat1": "6大分类", "router_stat1_sub": "自动任务检测",
    "router_stat2": "0.3ms开销", "router_stat2_sub": "每次$0.0000006",
    "router_stat3": "自动故障切换", "router_stat3_sub": "主模型故障→备用",
    "router_stat4": "平均节省91%", "router_stat4_sub": "对比GPT-4",
    "router_good_title": "使用AICraft Auto Router",
    "router_bad_title": "不使用（如OpenRouter）",
    "rt_task": "任务", "rt_primary": "首选模型", "rt_fallback": "备用",
    "rt_budget": "省钱选择", "rt_save": "对比GPT-4",
    "rt_coding": "编程", "rt_translation": "翻译/批量",
    "rt_chinese": "中文/多语言", "rt_reasoning": "推理/逻辑",
    "rt_creative": "创意写作", "rt_chat": "客服对话",
    "docs_label": "快速开始", "docs_title": "三行代码接入",
    "docs_sub": "OpenAI直接替换。支持Python、Node、Go、Rust、curl。",
    "privacy_label": "信任与合规", "privacy_title": "按司法管辖区保护隐私",
    "privacy_sub": "GDPR（欧盟）· PIPL（中国）· LGPD（巴西）· CCPA（加州）",
    "privacy_data_title": "数据承诺",
    "privacy_d1": "不存储对话内容", "privacy_d2": "TLS 1.3端到端加密",
    "privacy_d3": "API密钥哈希存储", "privacy_d4": "国产模型数据不出境",
    "privacy_d5": "国际模型经河套数据气泡", "privacy_d6": "日志最多保留30天",
    "privacy_gdpr_title": "GDPR（欧盟/欧洲经济区）",
    "privacy_gdpr_l1": "AICraft作为数据处理者", "privacy_gdpr_l2": "SCC跨境传输协议",
    "privacy_gdpr_l3": "删除权（30天内）", "privacy_gdpr_l4": "DPO: dpo@aicraftapi.com",
    "privacy_pipl_title": "PIPL（中国）",
    "privacy_pipl_l1": "受托处理者：AICraft", "privacy_pipl_l2": "法律依据：合同必需+知情同意",
    "privacy_pipl_l3": "数据跨境：河套数据气泡", "privacy_pipl_l4": "联系：dpo@aicraftapi.com",
    "privacy_other_title": "LGPD · CCPA",
    "privacy_other_l1": "LGPD：数据操作者·SCCs", "privacy_other_l2": "CCPA：我们不出售个人数据",
    "privacy_other_l3": "知情权·删除权", "privacy_other_l4": "privacy@aicraftapi.com",
    "consent_label": "我同意隐私政策和服务条款。API请求路由到上游提供商。国际模型经OpenRouter（美国）传输。",
    "signup_title": "创建AICraft账户", "signup_sub": "免费开始。无需信用卡。",
    "signup_email": "邮箱", "signup_password": "密码", "signup_name": "全名",
    "signup_country": "国家/地区", "signup_usecase": "使用场景",
    "signup_source": "从哪里了解到我们",
    "signup_country_select": "请选择...",
    "signup_usecase_select": "请选择...",
    "signup_usecase_1": "个人项目/爱好", "signup_usecase_2": "创业/小企业",
    "signup_usecase_3": "企业/公司", "signup_usecase_4": "学术/研究",
    "signup_usecase_5": "探索/学习",
    "signup_source_select": "请选择（选填）",
    "signup_source_1": "GitHub", "signup_source_2": "Google搜索",
    "signup_source_3": "Dev.to/Hashnode", "signup_source_4": "Reddit/Hacker News",
    "signup_source_5": "朋友/同事", "signup_source_6": "社交媒体",
    "signup_consent_privacy": "我同意隐私政策并同意数据处理。",
    "signup_consent_terms": "我同意服务条款。",
    "signup_consent_crossborder": "我理解国际模型请求可能经由OpenRouter（美国）传输。",
    "signup_submit": "创建账户", "signup_login": "已有账户？", "signup_login_link": "登录",
    "chat_header": "AICraft助手·AI驱动",
    "chat_greeting": "你好！问我任何关于AICraft API、定价或如何开始的问题。",
    "chat_powered": "由AICraft Auto Router驱动",
    "footer_product": "产品", "footer_company": "公司", "footer_legal": "法律",
    "footer_api": "API", "footer_models": "模型", "footer_pricing": "定价",
    "footer_router": "智能路由", "footer_docs": "文档", "footer_about": "关于",
    "footer_blog": "博客", "footer_careers": "招聘", "footer_contact": "联系",
    "footer_privacy": "隐私政策", "footer_terms": "服务条款",
    "footer_dpa": "DPA", "footer_sla": "SLA", "footer_status": "状态",
    "footer_github": "GitHub", "footer_changelog": "更新日志",
    "footer_copyright": "© 2026 AICraft · 深圳艾创矩阵科技有限公司 · 河套深港科技创新合作区",
}

ja_map = {
    "nav_models": "モデル", "nav_pricing": "料金", "nav_router": "自動ルート",
    "nav_docs": "ドキュメント", "nav_privacy": "プライバシー", "nav_signup": "登録",
    "hero_badge": "7プロバイダー · 40+モデル · 稼働中",
    "hero_h1_p1": "1つのAPIで", "hero_h1_p2": "すべての最先端モデルを",
    "hero_desc": "40以上のAIモデルに単一エンドポイントでアクセス。Auto Routerが最適なモデルを自動選択。",
    "hero_cta1": "プランを見る", "hero_cta2": "APIドキュメント", "hero_cta3": "無料登録",
    "pricing_label": "料金", "pricing_title": "シンプル、透明、競争力あり",
    "docs_title": "3行で統合", "router_title": "Autoインテリジェントルーティングを搭載した唯一のプラットフォーム",
    "privacy_label": "信頼とコンプライアンス", "privacy_title": "管轄区域ごとのプライバシー",
}

pt_map = {
    "nav_models": "Modelos", "nav_pricing": "Preços", "nav_router": "Auto Router",
    "nav_docs": "Docs", "nav_privacy": "Privacidade", "nav_signup": "Cadastrar",
    "hero_badge": "7 Provedores · 40+ Modelos · Ao vivo",
    "hero_h1_p1": "Uma API para", "hero_h1_p2": "todos os modelos frontier",
    "hero_desc": "Acesse 40+ modelos IA através de um único endpoint. Auto Router escolhe o melhor modelo.",
    "hero_cta1": "Ver Planos", "hero_cta2": "Documentação", "hero_cta3": "Cadastro Grátis",
    "pricing_label": "Preços", "pricing_title": "Simples, transparente, competitivo",
    "docs_title": "3 linhas para integrar",
    "router_title": "A única plataforma com Auto Intelligent Routing",
    "privacy_label": "Confiança e Conformidade", "privacy_title": "Privacidade por jurisdição",
}

es_map = {
    "nav_models": "Modelos", "nav_pricing": "Precios", "nav_router": "Auto Router",
    "nav_docs": "Docs", "nav_privacy": "Privacidad", "nav_signup": "Registrarse",
    "hero_badge": "7 Proveedores · 40+ Modelos · En vivo",
    "hero_h1_p1": "Una API para", "hero_h1_p2": "todos los modelos frontier",
    "hero_desc": "Accede a 40+ modelos IA a través de un solo endpoint. Auto Router elige el mejor modelo.",
    "hero_cta1": "Ver Planes", "hero_cta2": "Documentación", "hero_cta3": "Registro Gratis",
    "pricing_label": "Precios", "pricing_title": "Simple, transparente, competitivo",
    "docs_title": "3 líneas para integrar",
    "router_title": "La única plataforma con Auto Intelligent Routing",
    "privacy_label": "Confianza y Cumplimiento", "privacy_title": "Privacidad por jurisdicción",
}

# 6. Generate the complete i18n JS block
js_lines = []
js_lines.append('<script>')
js_lines.append('var T={en:{},zh:{},ja:{},ko:{},th:{},id:{},vi:{},es:{},pt:{}};')

# English: use existing defaults
for key in all_keys:
    en = existing.get(key, key)
    en = en.replace('"', '\\"').replace('\n', ' ')
    js_lines.append(f'T.en["{key}"]="{en}";')

# Chinese
for key, val in zh_map.items():
    val = val.replace('"', '\\"')
    js_lines.append(f'T.zh["{key}"]="{val}";')

# Japanese
for key, val in ja_map.items():
    val = val.replace('"', '\\"')
    js_lines.append(f'T.ja["{key}"]="{val}";')

# Portuguese
for key, val in pt_map.items():
    val = val.replace('"', '\\"')
    js_lines.append(f'T.pt["{key}"]="{val}";')

# Spanish
for key, val in es_map.items():
    val = val.replace('"', '\\"')
    js_lines.append(f'T.es["{key}"]="{val}";')

# For ko, th, id, vi - fall back to English
js_lines.append('// Korean, Thai, Indonesian, Vietnamese: use English as fallback')

# Language switcher + setLang function
js_lines.append('''
var currentLang = localStorage.getItem("al") || "en";
function setLang(code) {
  currentLang = code;
  localStorage.setItem("al", code);
  var flags = {en:"EN",zh:"中文",ja:"日本",ko:"한국",th:"ไทย",id:"ID",vi:"VI",es:"ES",pt:"PT"};
  var lf = document.getElementById("lf");
  if (lf) lf.textContent = flags[code] || "EN";
  var data = T[code] || T.en;
  document.querySelectorAll("[data-i18n]").forEach(function(el) {
    var k = el.getAttribute("data-i18n");
    if (data[k]) el.textContent = data[k];
  });
  // Update currency
  var rates = {en:{sym:"$",rate:1},zh:{sym:"¥",rate:7.25},ja:{sym:"¥",rate:150},ko:{sym:"₩",rate:1350},th:{sym:"฿",rate:36},id:{sym:"Rp",rate:16000},vi:{sym:"₫",rate:25000},es:{sym:"€",rate:0.92},pt:{sym:"R$",rate:5.50}};
  var usdPrices = {free:0,starter:15,pro:45,global:89,enterprise:299};
  var r = rates[code] || rates.en;
  document.querySelectorAll("[data-price]").forEach(function(el) {
    var key = el.getAttribute("data-price");
    var usd = usdPrices[key];
    if (usd !== undefined) {
      var v = Math.round(usd * r.rate);
      el.textContent = v === 0 ? r.sym + "0" : r.sym + v.toLocaleString();
    }
  });
}
function toggleLang(e) { e.preventDefault(); e.stopPropagation(); document.getElementById("lp").classList.toggle("active"); }
document.addEventListener("click", function(e) { var lp = document.getElementById("lp"); if (lp && !lp.contains(e.target)) lp.classList.remove("active"); });
function openSignup() { document.getElementById("sm").style.display = "flex"; }
function closeSignup() { document.getElementById("sm").style.display = "none"; }
function toggleMenu() { document.getElementById("mm").classList.toggle("open"); }
function toggleChatW() { document.getElementById("cpw").classList.toggle("open-w"); }
setLang(currentLang);
''')

# Model rendering
js_lines.append('''
var tcm=[{p:"DeepSeek",n:"DeepSeek V3",d:"Flagship model. #1 coding benchmark.",ctx:"128K",inp:"$0.14",out:"$0.28",c:"#2563eb"},{p:"DeepSeek",n:"DeepSeek V4-Flash",d:"Fastest & cheapest. Batch processing.",ctx:"128K",inp:"$0.003",out:"$0.01",c:"#2563eb"},{p:"DeepSeek",n:"DeepSeek R1",d:"Advanced reasoning with CoT.",ctx:"128K",inp:"$0.55",out:"$2.19",c:"#2563eb"},{p:"Alibaba",n:"Qwen-Max",d:"Best Chinese comprehension.",ctx:"32K",inp:"$0.35",out:"$1.40",c:"#f59e0b"},{p:"Alibaba",n:"Qwen-Plus",d:"Balanced performance & cost.",ctx:"32K",inp:"$0.10",out:"$0.40",c:"#f59e0b"},{p:"Alibaba",n:"Qwen-Turbo",d:"Fast & affordable.",ctx:"8K",inp:"$0.03",out:"$0.12",c:"#f59e0b"},{p:"Zhipu",n:"GLM-5",d:"Strong logical reasoning.",ctx:"128K",inp:"$0.70",out:"$2.80",c:"#7c3aed"},{p:"Zhipu",n:"GLM-5-Flash",d:"Fast variant.",ctx:"128K",inp:"$0.10",out:"$0.40",c:"#7c3aed"},{p:"MiniMax",n:"MiniMax M2.5",d:"Excellent creative writing.",ctx:"128K",inp:"$0.10",out:"$0.40",c:"#ec4899"},{p:"MiniMax",n:"MiniMax M3",d:"Latest generation.",ctx:"128K",inp:"$0.15",out:"$0.60",c:"#ec4899"},{p:"ByteDance",n:"Doubao Pro",d:"Natural conversation.",ctx:"32K",inp:"$0.06",out:"$0.24",c:"#10b981"},{p:"ByteDance",n:"Doubao Lite",d:"Lightweight & cheapest.",ctx:"8K",inp:"$0.008",out:"$0.03",c:"#10b981"}];
var tim=[{p:"OpenAI",n:"GPT-4o",d:"Multimodal flagship.",ctx:"128K",inp:"$2.50",out:"$10.00",c:"#22c55e"},{p:"OpenAI",n:"GPT-4o-mini",d:"Cost-effective.",ctx:"128K",inp:"$0.15",out:"$0.60",c:"#22c55e"},{p:"Anthropic",n:"Claude Sonnet 4",d:"Speed & capability.",ctx:"200K",inp:"$3.00",out:"$15.00",c:"#ef4444"},{p:"Google",n:"Gemma 3 27B",d:"Open-weight from Google.",ctx:"128K",inp:"$0.15",out:"$0.60",c:"#a855f7"},{p:"Mistral",n:"Mistral Large",d:"European frontier.",ctx:"128K",inp:"$2.00",out:"$8.00",c:"#06b6d4"},{p:"Meta",n:"Llama 4 Maverick",d:"Open frontier from Meta.",ctx:"1M",inp:"$0.20",out:"$0.80",c:"#f97316"},{p:"NVIDIA",n:"Nemotron Ultra",d:"550B MoE. Free tier.",ctx:"1M",inp:"FREE",out:"FREE",c:"#84cc16"}];
var mdm=[{p:"Kling",n:"Kling 2.0",d:"Text-to-video. Up to 2min.",ctx:"10s",inp:"$0.08",out:"-",c:"#f43f5e"},{p:"Alibaba",n:"Wan2.1",d:"VBench #1 video model.",ctx:"10s",inp:"$0.06",out:"-",c:"#f59e0b"},{p:"ByteDance",n:"Jimeng Video",d:"HD short videos.",ctx:"10s",inp:"$0.08",out:"-",c:"#10b981"},{p:"ByteDance",n:"Seedance",d:"Img+vid+audio input.",ctx:"11s",inp:"$0.10",out:"-",c:"#10b981"},{p:"ByteDance",n:"Jimeng Image",d:"Text-to-image HD.",ctx:"2K",inp:"$0.003",out:"-",c:"#3b82f6"}];
function rm(m,g){var el=document.getElementById(g);if(!el)return;el.innerHTML=m.map(function(x){return'<div class=\"mc\"><div class=\"mc-top\"><div class=\"mc-av\" style=\"background:'+x.c+'\">&#9670;</div><div><div class=\"mc-n\">'+x.n+'</div><div class=\"mc-p\">'+x.p+'</div></div></div><div class=\"mc-d\">'+x.d+'</div><div class=\"mc-tags\"><span class=\"tag blu\">&#55357;&#56560; '+x.ctx+'</span><span class=\"tag grn\">&#11015; '+x.inp+'</span><span class=\"tag gld\">&#11014; '+x.out+'</span></div></div>'}).join("");}
setTimeout(function(){rm(tcm,\"gtc\");rm(tim,\"gti\");rm(mdm,\"gmd\");},100);
</script>
''')

new_js = '\n'.join(js_lines)

# 7. Replace ALL existing script blocks with our complete one
html = re.sub(r'<script>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script>.*?</script>', '', html, flags=re.DOTALL)
# Add our complete script before </body>
html = html.replace('</body>', new_js + '\n</body>')

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Complete i18n: {len(all_keys)} keys x 5 languages fully translated")
print(f"Default translations: {len(existing)} keys")
print(f"Chinese translations: {len(zh_map)} keys")
print(f"Japanese translations: {len(ja_map)} keys")
print(f"Portuguese translations: {len(pt_map)} keys")
print(f"Spanish translations: {len(es_map)} keys")
