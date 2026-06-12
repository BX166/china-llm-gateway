"""Strip all complex JS, rebuild with dead-simple inline onclick"""

with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove ALL existing script blocks
import re
html = re.sub(r'<script>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r"<script>.*?</script>", '', html, flags=re.DOTALL)

# Now add ONE single clean script before </body>
clean_js = r"""<script>
// === Language data ===
var T={en:{},zh:{},ja:{},ko:{},th:{},id:{},vi:{},es:{},pt:{}};
function add(k,en,zh,ja,ko,th,id,vi,es,pt){T.en[k]=en;T.zh[k]=zh||en;T.ja[k]=ja||en;T.ko[k]=ko||en;T.th[k]=th||en;T.id[k]=id||en;T.vi[k]=vi||en;T.es[k]=es||en;T.pt[k]=pt||en;}
// Essential translations for Hero
add("hero_badge","7 Providers · 40+ Models · Live","7大渠道 · 40+模型 · 运行中","7プロバイダー · 40+モデル · 稼働中","7개 제공업체 · 40+ 모델 · 가동 중","7 ผู้ให้บริการ · 40+ โมเดล · ออนไลน์","7 Penyedia · 40+ Model · Aktif","7 Nhà cung cấp · 40+ Mô hình · Hoạt động","7 Proveedores · 40+ Modelos · En vivo","7 Provedores · 40+ Modelos · Ao vivo");
add("hero_title_p1","One API for","一个API","1つのAPIで","하나의 API로","หนึ่ง API สำหรับ","Satu API untuk","Một API cho","Una API para","Uma API para");
add("hero_title_p2","every frontier model","调用所有顶级模型","すべての最先端モデルを","모든 최첨단 모델을","ทุกโมเดลชั้นนำ","semua model frontier","mọi mô hình hàng đầu","todos los modelos frontier","todos os modelos frontier");
add("hero_desc","Access 40+ AI models through a single endpoint. Auto Router picks the best model for every task.","通过统一端点访问40+AI模型。Auto智能路由器自动选择最优模型。","40以上のAIモデルに単一エンドポイントでアクセス。Auto Routerが最適なモデルを自動選択。","40개 이상 AI 모델을 단일 엔드포인트로. Auto Router가 최적 모델 자동 선택.","40+ โมเดล AI ผ่านจุดเชื่อมต่อเดียว Auto Router เลือกโมเดลที่ดีที่สุด","40+ model AI melalui satu endpoint. Auto Router memilih model terbaik.","40+ mô hình AI qua một endpoint. Auto Router chọn mô hình tốt nhất.","40+ modelos IA a través de un solo endpoint. Auto Router elige el mejor modelo.","40+ modelos IA através de um único endpoint. Auto Router escolhe o melhor modelo.");
add("hero_cta1","View Plans","查看方案","プランを見る","요금제 보기","ดูแผน","Lihat Paket","Xem gói","Ver Planes","Ver Planos");
add("hero_cta2","API Docs","API文档","APIドキュメント","API 문서","เอกสาร API","Dokumen API","Tài liệu API","Documentación","Documentação");
// Quick i18n for all data-i18n elements
add("nav_models","Models","模型","モデル","모델","โมเดล","Model","Mô hình","Modelos","Modelos");
add("nav_pricing","Pricing","定价","料金","가격","ราคา","Harga","Giá","Precios","Preços");
add("nav_router","Auto Router","智能路由","自動ルート","자동라우팅","เส้นทางอัตโนมัติ","Rute Otomatis","Tự động","Auto Router","Auto Router");
add("nav_docs","Docs","文档","ドキュメント","문서","เอกสาร","Dokumen","Tài liệu","Docs","Docs");
add("nav_privacy","Privacy","隐私","プライバシー","개인정보","ความเป็นส่วนตัว","Privasi","Quyền riêng tư","Privacidad","Privacidade");

var currentLang = localStorage.getItem("al") || "en";

// Simple setLang function
function setLang(code) {
  currentLang = code;
  localStorage.setItem("al", code);

  // Update flag display
  var flags = {en:"EN",zh:"中文",ja:"日本",ko:"한국",th:"ไทย",id:"ID",vi:"VI",es:"ES",pt:"PT"};
  var lf = document.getElementById("lf");
  if (lf) lf.textContent = flags[code] || "EN";

  // Update all data-i18n elements
  var data = T[code] || T.en;
  var els = document.querySelectorAll("[data-i18n]");
  for (var i = 0; i < els.length; i++) {
    var k = els[i].getAttribute("data-i18n");
    if (data[k]) els[i].textContent = data[k];
  }

  // Update currency prices
  var rates = {en:{sym:"$",rate:1},zh:{sym:"¥",rate:7.25},ja:{sym:"¥",rate:150},ko:{sym:"₩",rate:1350},th:{sym:"฿",rate:36},id:{sym:"Rp",rate:16000},vi:{sym:"₫",rate:25000},es:{sym:"€",rate:0.92},pt:{sym:"R$",rate:5.50}};
  var usdPrices = {free:0,starter:15,pro:45,global:89,enterprise:299};
  var r = rates[code] || rates.en;
  var priceEls = document.querySelectorAll("[data-price]");
  for (var i = 0; i < priceEls.length; i++) {
    var key = priceEls[i].getAttribute("data-price");
    var usd = usdPrices[key];
    if (usd !== undefined) {
      var v = Math.round(usd * r.rate);
      priceEls[i].textContent = v === 0 ? r.sym + "0" : r.sym + v.toLocaleString();
    }
  }
}

// Close language dropdown when clicking outside
document.addEventListener("click", function(e) {
  var lp = document.getElementById("lp");
  if (lp && !lp.contains(e.target)) lp.classList.remove("active");
});

// Toggle language dropdown
function toggleLang(e) {
  e.preventDefault();
  e.stopPropagation();
  document.getElementById("lp").classList.toggle("active");
}

// Signup modal
function openSignup() { document.getElementById("sm").style.display = "flex"; }
function closeSignup() { document.getElementById("sm").style.display = "none"; }

// Mobile menu
function toggleMenu() { document.getElementById("mm").classList.toggle("open"); }

// Chat widget
function toggleChatW() { document.getElementById("cpw").classList.toggle("open-w"); }

// Initialize on load
setLang(currentLang);

// Model grids (static data, simple rendering)
var tcm=[{p:"DeepSeek",n:"DeepSeek V3",d:"Flagship model. #1 coding benchmark.",ctx:"128K",inp:"$0.14",out:"$0.28",c:"#2563eb"},{p:"DeepSeek",n:"DeepSeek V4-Flash",d:"Fastest & cheapest. Batch processing.",ctx:"128K",inp:"$0.003",out:"$0.01",c:"#2563eb"},{p:"DeepSeek",n:"DeepSeek R1",d:"Advanced reasoning with CoT.",ctx:"128K",inp:"$0.55",out:"$2.19",c:"#2563eb"},{p:"Alibaba",n:"Qwen-Max",d:"Best Chinese comprehension.",ctx:"32K",inp:"$0.35",out:"$1.40",c:"#f59e0b"},{p:"Alibaba",n:"Qwen-Plus",d:"Balanced performance & cost.",ctx:"32K",inp:"$0.10",out:"$0.40",c:"#f59e0b"},{p:"Alibaba",n:"Qwen-Turbo",d:"Fast & affordable.",ctx:"8K",inp:"$0.03",out:"$0.12",c:"#f59e0b"},{p:"Zhipu",n:"GLM-5",d:"Strong logical reasoning.",ctx:"128K",inp:"$0.70",out:"$2.80",c:"#7c3aed"},{p:"Zhipu",n:"GLM-5-Flash",d:"Fast variant.",ctx:"128K",inp:"$0.10",out:"$0.40",c:"#7c3aed"},{p:"MiniMax",n:"MiniMax M2.5",d:"Excellent creative writing.",ctx:"128K",inp:"$0.10",out:"$0.40",c:"#ec4899"},{p:"MiniMax",n:"MiniMax M3",d:"Latest generation.",ctx:"128K",inp:"$0.15",out:"$0.60",c:"#ec4899"},{p:"ByteDance",n:"Doubao Pro",d:"Natural conversation.",ctx:"32K",inp:"$0.06",out:"$0.24",c:"#10b981"},{p:"ByteDance",n:"Doubao Lite",d:"Lightweight & cheapest.",ctx:"8K",inp:"$0.008",out:"$0.03",c:"#10b981"}];
var tim=[{p:"OpenAI",n:"GPT-4o",d:"Multimodal flagship.",ctx:"128K",inp:"$2.50",out:"$10.00",c:"#22c55e"},{p:"OpenAI",n:"GPT-4o-mini",d:"Cost-effective.",ctx:"128K",inp:"$0.15",out:"$0.60",c:"#22c55e"},{p:"Anthropic",n:"Claude Sonnet 4",d:"Speed & capability.",ctx:"200K",inp:"$3.00",out:"$15.00",c:"#ef4444"},{p:"Google",n:"Gemma 3 27B",d:"Open-weight from Google.",ctx:"128K",inp:"$0.15",out:"$0.60",c:"#a855f7"},{p:"Mistral",n:"Mistral Large",d:"European frontier.",ctx:"128K",inp:"$2.00",out:"$8.00",c:"#06b6d4"},{p:"Meta",n:"Llama 4 Maverick",d:"Open frontier from Meta.",ctx:"1M",inp:"$0.20",out:"$0.80",c:"#f97316"},{p:"NVIDIA",n:"Nemotron Ultra",d:"550B MoE. Free tier.",ctx:"1M",inp:"FREE",out:"FREE",c:"#84cc16"}];
var mdm=[{p:"Kling",n:"Kling 2.0",d:"Text-to-video. Up to 2min.",ctx:"10s",inp:"$0.08",out:"-",c:"#f43f5e"},{p:"Alibaba",n:"Wan2.1",d:"VBench #1 video model.",ctx:"10s",inp:"$0.06",out:"-",c:"#f59e0b"},{p:"ByteDance",n:"Jimeng Video",d:"HD short videos.",ctx:"10s",inp:"$0.08",out:"-",c:"#10b981"},{p:"ByteDance",n:"Seedance",d:"Img+vid+audio input.",ctx:"11s",inp:"$0.10",out:"-",c:"#10b981"},{p:"ByteDance",n:"Jimeng Image",d:"Text-to-image HD.",ctx:"2K",inp:"$0.003",out:"-",c:"#3b82f6"}];
function rm(m,g){var el=document.getElementById(g);if(!el)return;el.innerHTML=m.map(function(x){return'<div class="mc"><div class="mc-top"><div class="mc-av" style="background:'+x.c+'">&#9670;</div><div><div class="mc-n">'+x.n+'</div><div class="mc-p">'+x.p+'</div></div></div><div class="mc-d">'+x.d+'</div><div class="mc-tags"><span class="tag blu">📐 '+x.ctx+'</span><span class="tag grn">⬇ '+x.inp+'</span><span class="tag gld">⬆ '+x.out+'</span></div></div>'}).join("");}
setTimeout(function(){rm(tcm,"gtc");rm(tim,"gti");rm(mdm,"gmd");},100);
</script>"""

html = re.sub(r'</body>', clean_js + '\n</body>', html)

# Update lang trigger button to use toggleLang
html = html.replace(
    'onclick="document.getElementById(\'lp\').classList.toggle(\'active\');return false;"',
    'onclick="toggleLang(event)"'
)

# Update signup button onclicks - make sure they call openSignup()
# Check all signup buttons
html = html.replace(
    'onclick="openSignup()"',
    'onclick="openSignup()"'
)

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("All JS rebuilt with simple inline onclick")
