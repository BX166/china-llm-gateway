#!/usr/bin/env python3
"""Add full i18n to AICraft v3 site"""

with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ===== STEP 1: Add data-i18n attributes to all text elements =====

replacements = [
    # Nav
    ('<a href="#models">Models</a>', '<a href="#models" data-i18n="nav_models">Models</a>'),
    ('<a href="#pricing">Pricing</a>', '<a href="#pricing" data-i18n="nav_pricing">Pricing</a>'),
    ('<a href="#router">Auto Router</a>', '<a href="#router" data-i18n="nav_router">Auto Router</a>'),
    ('<a href="#docs">Docs</a>', '<a href="#docs" data-i18n="nav_docs">Docs</a>'),
    ('<a href="#privacy">Privacy</a>', '<a href="#privacy" data-i18n="nav_privacy">Privacy</a>'),
    ('<a href="#models" onclick="toggleMenu()">Models</a>', '<a href="#models" onclick="toggleMenu()" data-i18n="nav_models">Models</a>'),
    ('<a href="#pricing" onclick="toggleMenu()">Pricing</a>', '<a href="#pricing" onclick="toggleMenu()" data-i18n="nav_pricing">Pricing</a>'),
    ('<a href="#router" onclick="toggleMenu()">Auto Router</a>', '<a href="#router" onclick="toggleMenu()" data-i18n="nav_router">Auto Router</a>'),
    ('<a href="#docs" onclick="toggleMenu()">Docs</a>', '<a href="#docs" onclick="toggleMenu()" data-i18n="nav_docs">Docs</a>'),
    ('<a href="#privacy" onclick="toggleMenu()">Privacy</a>', '<a href="#privacy" onclick="toggleMenu()" data-i18n="nav_privacy">Privacy</a>'),
    ('Sign Up', 'Sign Up',),  # Will handle differently

    # Hero
    ('<div class="sec-label">Model Library</div>', '<div class="sec-label" data-i18n="models_label">Model Library</div>'),
    ('<h2 class="sec-title">Every model, one endpoint</h2>', '<h2 class="sec-title" data-i18n="models_title">Every model, one endpoint</h2>'),
    ('<p class="sec-sub">40+ models across 7 providers. Text generation, video creation, image synthesis — all behind a single API key.</p>', '<p class="sec-sub" data-i18n="models_sub">40+ models across 7 providers. Text generation, video creation, image synthesis — all behind a single API key.</p>'),

    # Tabs
    ('>Text · Chinese<', ' data-i18n="tab_text_chinese">Text · Chinese<'),
    ('>Text · International<', ' data-i18n="tab_text_intl">Text · International<'),
    ('>Media Gen<', ' data-i18n="tab_media">Media Gen<'),

    # Pricing
    ('<div class="sec-label">Pricing</div>', '<div class="sec-label" data-i18n="pricing_label">Pricing</div>',),
    ('<h2 class="sec-title">Simple, transparent, competitive</h2>', '<h2 class="sec-title" data-i18n="pricing_title">Simple, transparent, competitive</h2>'),
    ('<p class="sec-sub" style="margin-bottom:30px;">All plans include OpenAI-compatible API + Auto Router. Pay only for what you use beyond included tokens.</p>', '<p class="sec-sub" style="margin-bottom:30px;" data-i18n="pricing_sub">All plans include OpenAI-compatible API + Auto Router. Pay only for what you use beyond included tokens.</p>'),

    # Pricing cards - labels
    ('>Free<', ' data-i18n="price_free">Free<'),
    ('>5M tokens · Chinese models<', ' data-i18n="price_free_tokens">5M tokens · Chinese models<'),
    ('>All Chinese text models<', ' data-i18n="price_free_feat1">All Chinese text models<'),
    ('>5 requests/min<', ' data-i18n="price_free_feat2">5 requests/min<'),
    ('>Auto Router included<', ' data-i18n="price_free_feat3">Auto Router included<'),
    ('>Community support<', ' data-i18n="price_free_feat4">Community support<'),
    ('>Start Free<', ' data-i18n="price_free_cta">Start Free<'),

    # Router
    ('<div class="sec-label">Competitive Edge</div>', '<div class="sec-label" data-i18n="router_label">Competitive Edge</div>'),
    ('<h2 class="sec-title">The only platform with Auto Intelligent Routing</h2>', '<h2 class="sec-title" data-i18n="router_title">The only platform with Auto Intelligent Routing</h2>'),
    ('<p class="sec-sub">OpenRouter doesn\'t have it. SiliconFlow doesn\'t have it. Qiniu doesn\'t have it. Only AICraft automatically selects the optimal model for every request.</p>', '<p class="sec-sub" data-i18n="router_sub">OpenRouter doesn\'t have it. SiliconFlow doesn\'t have it. Qiniu doesn\'t have it. Only AICraft automatically selects the optimal model for every request.</p>'),

    # Router cards
    ('>6 Categories<', ' data-i18n="router_cat1">6 Categories<'),
    ('>Auto task detection<', ' data-i18n="router_cat1_sub">Auto task detection<'),
    ('>0.3ms Overhead<', ' data-i18n="router_cat2">0.3ms Overhead<'),
    ('>$0.0000006 per call<', ' data-i18n="router_cat2_sub">$0.0000006 per call<'),
    ('>Auto Fallback<', ' data-i18n="router_cat3">Auto Fallback<'),
    ('>Primary fails → backup<', ' data-i18n="router_cat3_sub">Primary fails → backup<'),
    ('>91% Avg Saving<', ' data-i18n="router_cat4">91% Avg Saving<'),
    ('>vs GPT-4<', ' data-i18n="router_cat4_sub">vs GPT-4<'),

    # Docs
    ('<div class="sec-label" style="color:#fbbf24;">Quick Start</div>', '<div class="sec-label" style="color:#fbbf24;" data-i18n="docs_label">Quick Start</div>'),
    ('<h2 class="sec-title" style="color:#fff;">3 lines to integrate</h2>', '<h2 class="sec-title" style="color:#fff;" data-i18n="docs_title">3 lines to integrate</h2>'),
    ('<p class="sec-sub" style="color:#94a3b8;">Drop-in replacement for OpenAI. Works with Python, Node, Go, Rust, curl — any HTTP client.</p>', '<p class="sec-sub" style="color:#94a3b8;" data-i18n="docs_sub">Drop-in replacement for OpenAI. Works with Python, Node, Go, Rust, curl — any HTTP client.</p>'),

    # Privacy
    ('<div class="sec-label">Trust & Compliance</div>', '<div class="sec-label" data-i18n="privacy_label">Trust & Compliance</div>'),
    ('<h2 class="sec-title">Privacy by jurisdiction</h2>', '<h2 class="sec-title" data-i18n="privacy_title">Privacy by jurisdiction</h2>'),
    ('<p class="sec-sub">GDPR (EU) · PIPL (China) · LGPD (Brazil) · CCPA (California)</p>', '<p class="sec-sub" data-i18n="privacy_sub">GDPR (EU) · PIPL (China) · LGPD (Brazil) · CCPA (California)</p>'),

    # Footer - use labels
    ('>Product<', ' data-i18n="footer_product">Product<'),
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)

# ===== STEP 2: Add comprehensive i18n data =====
i18n_js = """
<script>
var langs=[{code:"en",name:"English",flag:"EN"},{code:"zh",name:"中文",flag:"中文"},{code:"ja",name:"日本語",flag:"日本"},{code:"ko",name:"한국어",flag:"한국"},{code:"th",name:"ไทย",flag:"ไทย"},{code:"id",name:"Bahasa Indonesia",flag:"ID"},{code:"vi",name:"Tiếng Việt",flag:"VI"},{code:"es",name:"Español",flag:"ES"},{code:"pt",name:"Português",flag:"PT"}];
var i18n={en:{},zh:{},ja:{},ko:{},th:{},id:{},vi:{},es:{},pt:{}};

function T(en,zh,ja,ko,th,id,vi,es,pt){
  i18n.en[en.key]=en.val;i18n.zh[en.key]=zh||en.val;i18n.ja[en.key]=ja||en.val;
  i18n.ko[en.key]=ko||en.val;i18n.th[en.key]=th||en.val;i18n.id[en.key]=id||en.val;
  i18n.vi[en.key]=vi||en.val;i18n.es[en.key]=es||en.val;i18n.pt[en.key]=pt||en.val;
}

// Build using key:value pairs
function add(k,v){i18n.en[k]=v}
add("nav_models","Models");add("nav_pricing","Pricing");add("nav_router","Auto Router");add("nav_docs","Docs");add("nav_privacy","Privacy");
add("hero_badge","7 Providers · 40+ Models · Live");
add("hero_title_p1","One API for");
add("hero_title_p2","every frontier model");
add("hero_desc","Access DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter & more through a single endpoint. Our Auto Router picks the best model for every task — saving up to 93% vs GPT-4.");
add("hero_cta1","View Plans");add("hero_cta2","API Docs");add("hero_cta3","Create Free Account");
add("models_label","Model Library");add("models_title","Every model, one endpoint");
add("models_sub","40+ models across 7 providers. Text generation, video creation, image synthesis — all behind a single API key.");
add("tab_text_chinese","Text · Chinese");add("tab_text_intl","Text · International");add("tab_media","Media Gen");
add("pricing_label","Pricing");add("pricing_title","Simple, transparent, competitive");
add("pricing_sub","All plans include OpenAI-compatible API + Auto Router. Pay only for what you use beyond included tokens.");
add("router_label","Competitive Edge");add("router_title","The only platform with Auto Intelligent Routing");
add("router_sub","OpenRouter doesn't have it. SiliconFlow doesn't have it. Qiniu doesn't have it. Only AICraft automatically selects the optimal model for every request.");
add("router_cat1","6 Categories");add("router_cat2","0.3ms Overhead");add("router_cat3","Auto Fallback");add("router_cat4","91% Avg Saving");
add("router_cat1_sub","Auto task detection");add("router_cat2_sub","$0.0000006 per call");
add("router_cat3_sub","Primary fails → backup");add("router_cat4_sub","vs GPT-4");
add("docs_label","Quick Start");add("docs_title","3 lines to integrate");
add("docs_sub","Drop-in replacement for OpenAI. Works with Python, Node, Go, Rust, curl — any HTTP client.");
add("privacy_label","Trust & Compliance");add("privacy_title","Privacy by jurisdiction");
add("privacy_sub","GDPR (EU) · PIPL (China) · LGPD (Brazil) · CCPA (California)");

// Chinese
function zhAdd(k,v){i18n.zh[k]=v}
zhAdd("nav_models","模型");zhAdd("nav_pricing","定价");zhAdd("nav_router","智能路由");zhAdd("nav_docs","文档");zhAdd("nav_privacy","隐私");
zhAdd("hero_badge","7大渠道 · 40+模型 · 运行中");
zhAdd("hero_title_p1","一个API");zhAdd("hero_title_p2","调用所有顶级模型");
zhAdd("hero_desc","通过统一端点访问DeepSeek、Qwen、GLM、MiniMax、豆包、OpenRouter等40+模型。Auto智能路由器自动为每项任务选择最优模型——相较GPT-4最高节省93%。");
zhAdd("hero_cta1","查看方案");zhAdd("hero_cta2","API文档");zhAdd("hero_cta3","免费注册");
zhAdd("models_label","模型库");zhAdd("models_title","每一个模型，一个端点");
zhAdd("models_sub","7大渠道40+模型。文本生成、视频创作、图片合成——全部统一API密钥。");
zhAdd("tab_text_chinese","文本·国产");zhAdd("tab_text_intl","文本·国际");zhAdd("tab_media","媒体生成");
zhAdd("pricing_label","定价");zhAdd("pricing_title","简单、透明、有竞争力");
zhAdd("pricing_sub","所有套餐含OpenAI兼容API+Auto Router。超额按量计费。");
zhAdd("router_label","竞争优势");zhAdd("router_title","唯一拥有Auto智能路由的平台");
zhAdd("router_sub","OpenRouter没有。硅基流动没有。七牛云没有。只有AICraft自动为每个请求选择最优模型。");
zhAdd("router_cat1","6大分类");zhAdd("router_cat2","0.3ms开销");zhAdd("router_cat3","自动故障切换");zhAdd("router_cat4","平均节省91%");
zhAdd("router_cat1_sub","自动任务检测");zhAdd("router_cat2_sub","每次$0.0000006");
zhAdd("router_cat3_sub","主模型故障→备用");zhAdd("router_cat4_sub","对比GPT-4");
zhAdd("docs_label","快速开始");zhAdd("docs_title","三行代码接入");
zhAdd("docs_sub","OpenAI直接替换。支持Python、Node、Go、Rust、curl——任何HTTP客户端。");
zhAdd("privacy_label","信任与合规");zhAdd("privacy_title","按司法管辖区保护隐私");
zhAdd("privacy_sub","GDPR（欧盟）· PIPL（中国）· LGPD（巴西）· CCPA（加州）");

// Japanese
function jaAdd(k,v){i18n.ja[k]=v}
jaAdd("nav_models","モデル");jaAdd("nav_pricing","料金");jaAdd("nav_router","自動ルート");jaAdd("nav_docs","ドキュメント");jaAdd("nav_privacy","プライバシー");
jaAdd("hero_badge","7プロバイダー · 40+モデル · 稼働中");
jaAdd("hero_title_p1","1つのAPIで");jaAdd("hero_title_p2","すべての最先端モデルを");
jaAdd("hero_desc","DeepSeek、Qwen、GLM、MiniMax、Doubao、OpenRouterなど40以上のモデルに単一エンドポイントでアクセス。Auto Routerが各タスクに最適なモデルを自動選択——GPT-4比最大93%削減。");
jaAdd("hero_cta1","プランを見る");jaAdd("hero_cta2","APIドキュメント");jaAdd("hero_cta3","無料登録");
jaAdd("models_label","モデルライブラリ");jaAdd("models_title","すべてのモデル、1つのエンドポイント");
jaAdd("models_sub","7プロバイダー40以上のモデル。テキスト、動画、画像生成すべて単一のAPIキーで。");
jaAdd("tab_text_chinese","テキスト·中国");jaAdd("tab_text_intl","テキスト·国際");jaAdd("tab_media","メディア生成");
jaAdd("pricing_label","料金");jaAdd("pricing_title","シンプル、透明、競争力あり");
jaAdd("pricing_sub","全プランにOpenAI互換APIとAuto Routerが含まれます。");
jaAdd("router_label","競争優位");jaAdd("router_title","Autoインテリジェントルーティングを搭載した唯一のプラットフォーム");
jaAdd("router_sub","OpenRouterにはない。SiliconFlowにもない。Qiniuにもない。AICraftだけが各リクエストに最適なモデルを自動選択します。");
jaAdd("router_cat1","6カテゴリ");jaAdd("router_cat2","0.3msオーバーヘッド");jaAdd("router_cat3","自動フォールバック");jaAdd("router_cat4","平均91%削減");
jaAdd("docs_label","クイックスタート");jaAdd("docs_title","3行で統合");
jaAdd("docs_sub","OpenAIの代替として。Python、Node、Go、Rust、curlで動作。");

// Korean
function koAdd(k,v){i18n.ko[k]=v}
koAdd("nav_models","모델");koAdd("nav_pricing","가격");koAdd("nav_router","자동라우팅");koAdd("nav_docs","문서");koAdd("nav_privacy","개인정보");
koAdd("hero_title_p1","하나의 API로");koAdd("hero_title_p2","모든 최첨단 모델을");
koAdd("hero_desc","DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter 등 40개 이상 모델을 단일 엔드포인트로. Auto Router가 최적 모델 자동 선택 — GPT-4 대비 최대 93% 절감.");
koAdd("hero_cta1","요금제 보기");koAdd("hero_cta2","API 문서");koAdd("hero_cta3","무료 가입");
koAdd("router_label","경쟁 우위");koAdd("router_title","Auto 지능형 라우팅을 갖춘 유일한 플랫폼");
koAdd("router_sub","OpenRouter에도, SiliconFlow에도, Qiniu에도 없습니다. AICraft만이 각 요청에 최적의 모델을 자동 선택합니다.");
koAdd("docs_label","빠른 시작");koAdd("docs_title","3줄로 통합");

// Thai
function thAdd(k,v){i18n.th[k]=v}
thAdd("nav_models","โมเดล");thAdd("nav_pricing","ราคา");thAdd("hero_title_p1","หนึ่ง API สำหรับ");thAdd("hero_title_p2","ทุกโมเดลชั้นนำ");
thAdd("hero_desc","เข้าถึง DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter และอีกมากมายผ่านจุดเชื่อมต่อเดียว Auto Router เลือกโมเดลที่ดีที่สุด — ประหยัดสูงสุด 93% เทียบ GPT-4");
thAdd("hero_cta1","ดูแผน");thAdd("hero_cta2","เอกสาร API");thAdd("hero_cta3","สมัครฟรี");
thAdd("router_title","แพลตฟอร์มเดียวที่มี Auto Intelligent Routing");
thAdd("docs_title","3 บรรทัดเพื่อผสานรวม");

// Indonesian
function idAdd(k,v){i18n.id[k]=v}
idAdd("nav_models","Model");idAdd("nav_pricing","Harga");idAdd("hero_title_p1","Satu API untuk");idAdd("hero_title_p2","semua model frontier");
idAdd("hero_desc","Akses DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter & lebih melalui satu endpoint. Auto Router memilih model terbaik — hemat hingga 93% vs GPT-4.");
idAdd("hero_cta1","Lihat Paket");idAdd("hero_cta2","Dokumen API");idAdd("hero_cta3","Daftar Gratis");
idAdd("router_title","Satu-satunya platform dengan Auto Intelligent Routing");
idAdd("docs_title","3 baris untuk integrasi");

// Vietnamese
function viAdd(k,v){i18n.vi[k]=v}
viAdd("nav_models","Mô hình");viAdd("nav_pricing","Giá");viAdd("hero_title_p1","Một API cho");viAdd("hero_title_p2","mọi mô hình hàng đầu");
viAdd("hero_desc","Truy cập DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter qua một endpoint. Auto Router chọn mô hình tốt nhất — tiết kiệm đến 93% so với GPT-4.");
viAdd("hero_cta1","Xem gói");viAdd("hero_cta2","Tài liệu API");viAdd("hero_cta3","Đăng ký miễn phí");
viAdd("router_title","Nền tảng duy nhất có Auto Intelligent Routing");
viAdd("docs_title","3 dòng để tích hợp");

// Spanish
function esAdd(k,v){i18n.es[k]=v}
esAdd("nav_models","Modelos");esAdd("nav_pricing","Precios");esAdd("hero_title_p1","Una API para");esAdd("hero_title_p2","todos los modelos frontier");
esAdd("hero_desc","Accede a DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter y más a través de un solo endpoint. Auto Router elige el mejor modelo — ahorra hasta 93% vs GPT-4.");
esAdd("hero_cta1","Ver Planes");esAdd("hero_cta2","Documentación");esAdd("hero_cta3","Registro Gratis");
esAdd("router_title","La única plataforma con Auto Intelligent Routing");
esAdd("docs_title","3 líneas para integrar");

// Portuguese
function ptAdd(k,v){i18n.pt[k]=v}
ptAdd("nav_models","Modelos");ptAdd("nav_pricing","Preços");ptAdd("hero_title_p1","Uma API para");ptAdd("hero_title_p2","todos os modelos frontier");
ptAdd("hero_desc","Acesse DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter e mais através de um único endpoint. Auto Router escolhe o melhor modelo — economize até 93% vs GPT-4.");
ptAdd("hero_cta1","Ver Planos");ptAdd("hero_cta2","Documentação");ptAdd("hero_cta3","Cadastro Grátis");
ptAdd("router_title","A única plataforma com Auto Intelligent Routing");
ptAdd("docs_title","3 linhas para integrar");

// Lang switcher logic
var drop=document.getElementById("lang-drop");
langs.forEach(function(l){var a=document.createElement("a");a.href="#";a.textContent=l.flag+" "+l.name;a.onclick=function(e){e.preventDefault();setLang(l.code)};drop.appendChild(a)});
document.getElementById("lang-trigger").onclick=function(e){e.preventDefault();e.stopPropagation();document.getElementById("lang-picker").classList.toggle("active")};
document.addEventListener("click",function(e){if(!document.getElementById("lang-picker").contains(e.target))document.getElementById("lang-picker").classList.remove("active")});

function setLang(code){
  var l=langs.find(function(x){return x.code===code})||langs[0];
  document.getElementById("lang-flag").textContent=l.flag;
  localStorage.setItem("aicraft-lang",code);
  var d=i18n[code]||i18n.en;
  document.querySelectorAll("[data-i18n]").forEach(function(el){
    var key=el.getAttribute("data-i18n");
    if(d[key])el.textContent=d[key];
  });
  document.querySelectorAll(".lang-drop a").forEach(function(a){
    a.classList.remove("sel");
    if(a.textContent.includes(l.name))a.classList.add("sel");
  });
}
setLang(localStorage.getItem("aicraft-lang")||"en");
</script>
"""

# Remove old lang script
import re
html = re.sub(r'<script>\s*// Language switcher.*?</script>', '', html, flags=re.DOTALL)

# Add new i18n script before </body>
html = html.replace("</body>", i18n_js + "\n</body>")

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Full i18n added OK")
