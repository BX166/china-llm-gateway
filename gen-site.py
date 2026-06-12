#!/usr/bin/env python3
"""Generate complete AICraft site with full i18n coverage"""
import json

# ========== COMPLETE i18n Dictionary ==========
T = {
"en":{},"zh":{},"ja":{},"ko":{},"th":{},"id":{},"vi":{},"es":{},"pt":{}
}
def add(key,en,zh,ja,ko,th,id,vi,es,pt):
    for lang,val in [("en",en),("zh",zh),("ja",ja),("ko",ko),("th",th),("id",id),("vi",vi),("es",es),("pt",pt)]:
        T[lang][key]=val

# Nav
add("nav_models","Models","模型","モデル","모델","โมเดล","Model","Mô hình","Modelos","Modelos")
add("nav_pricing","Pricing","定价","料金","가격","ราคา","Harga","Giá","Precios","Preços")
add("nav_router","Auto Router","智能路由","自動ルート","자동라우팅","เส้นทางอัตโนมัติ","Rute Otomatis","Tự động","Auto Router","Auto Router")
add("nav_docs","Docs","文档","ドキュメント","문서","เอกสาร","Dokumen","Tài liệu","Docs","Docs")
add("nav_privacy","Privacy","隐私","プライバシー","개인정보","ความเป็นส่วนตัว","Privasi","Quyền riêng tư","Privacidad","Privacidade")
add("nav_signup","Sign Up","注册","登録","가입","สมัคร","Daftar","Đăng ký","Registrarse","Cadastrar")

# Hero
add("hero_badge","7 Providers · 40+ Models · Live","7大渠道 · 40+模型 · 运行中","7プロバイダー · 40+モデル · 稼働中","7개 제공업체 · 40+ 모델 · 가동 중","7 ผู้ให้บริการ · 40+ โมเดล · ออนไลน์","7 Penyedia · 40+ Model · Aktif","7 Nhà cung cấp · 40+ Mô hình · Hoạt động","7 Proveedores · 40+ Modelos · En vivo","7 Provedores · 40+ Modelos · Ao vivo")
add("hero_h1_p1","One API for","一个API","1つのAPIで","하나의 API로","หนึ่ง API สำหรับ","Satu API untuk","Một API cho","Una API para","Uma API para")
add("hero_h1_p2","every frontier model","调用所有顶级模型","すべての最先端モデルを","모든 최첨단 모델을","ทุกโมเดลชั้นนำ","semua model frontier","mọi mô hình hàng đầu","todos los modelos frontier","todos os modelos frontier")
add("hero_desc","Access DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter & more through a single endpoint. Our Auto Router picks the best model for every task — saving up to 93% vs GPT-4.","通过统一端点访问DeepSeek、Qwen、GLM、MiniMax、豆包、OpenRouter等40+模型。Auto智能路由器自动为每项任务选择最优模型——相较GPT-4最高节省93%。","DeepSeek、Qwen、GLM、MiniMax、Doubao、OpenRouterなど40以上のモデルに単一エンドポイントでアクセス。Auto Routerが各タスクに最適なモデルを自動選択——GPT-4比最大93%削減。","DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter 등 40개 이상 모델을 단일 엔드포인트로. Auto Router가 최적 모델 자동 선택 — GPT-4 대비 최대 93% 절감.","เข้าถึง DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter และอีกมากมายผ่านจุดเชื่อมต่อเดียว Auto Router เลือกโมเดลที่ดีที่สุด — ประหยัดสูงสุด 93% เทียบ GPT-4","Akses DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter & lebih melalui satu endpoint. Auto Router memilih model terbaik — hemat hingga 93% vs GPT-4.","Truy cập DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter qua một endpoint. Auto Router chọn mô hình tốt nhất — tiết kiệm đến 93% so với GPT-4.","Accede a DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter y más a través de un solo endpoint. Auto Router elige el mejor modelo — ahorra hasta 93% vs GPT-4.","Acesse DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter e mais através de um único endpoint. Auto Router escolhe o melhor modelo — economize até 93% vs GPT-4.")
add("hero_cta1","View Plans","查看方案","プランを見る","요금제 보기","ดูแผน","Lihat Paket","Xem gói","Ver Planes","Ver Planos")
add("hero_cta2","API Docs","API文档","APIドキュメント","API 문서","เอกสาร API","Dokumen API","Tài liệu API","Documentación","Documentação")
add("hero_cta3","Create Free Account","免费注册","無料登録","무료 가입","สมัครฟรี","Daftar Gratis","Đăng ký miễn phí","Registro Gratis","Cadastro Grátis")

# Models
add("models_label","Model Library","模型库","モデルライブラリ","모델 라이브러리","คลังโมเดล","Perpustakaan Model","Thư viện mô hình","Biblioteca de Modelos","Biblioteca de Modelos")
add("models_title","Every model, one endpoint","每一个模型，一个端点","すべてのモデル、1つのエンドポイント","모든 모델, 하나의 엔드포인트","ทุกโมเดล หนึ่งจุดเชื่อมต่อ","Setiap model, satu endpoint","Mọi mô hình, một endpoint","Cada modelo, un endpoint","Cada modelo, um endpoint")
add("models_sub","40+ models across 7 providers. Text generation, video creation, image synthesis — all behind a single API key.","7大渠道40+模型。文本生成、视频创作、图片合成——全部统一API密钥。","7プロバイダー40以上のモデル。テキスト、動画、画像生成すべて単一のAPIキーで。","7개 제공업체 40+ 모델. 텍스트, 비디오, 이미지 생성 모두 단일 API 키로.","7 ผู้ให้บริการ 40+ โมเดล การสร้างข้อความ วิดีโอ รูปภาพ — ทั้งหมดด้วยคีย์ API เดียว","7 penyedia 40+ model. Teks, video, gambar — semua di balik satu kunci API.","7 nhà cung cấp 40+ mô hình. Văn bản, video, hình ảnh — tất cả sau một khóa API.","40+ modelos en 7 proveedores. Texto, video, imágenes — todo con una sola clave API.","40+ modelos em 7 provedores. Texto, vídeo, imagens — tudo com uma única chave API.")
add("tab_text_chinese","Text · Chinese","文本·国产","テキスト·中国","텍스트·중국","ข้อความ·จีน","Teks·China","Văn bản·Trung Quốc","Texto·Chino","Texto·Chinês")
add("tab_text_intl","Text · International","文本·国际","テキスト·国際","텍스트·국제","ข้อความ·นานาชาติ","Teks·Internasional","Văn bản·Quốc tế","Texto·Internacional","Texto·Internacional")
add("tab_media","Media Gen","媒体生成","メディア生成","미디어 생성","สร้างสื่อ","Media Gen","Tạo phương tiện","Gen Media","Gerar Mídia")

# Pricing cards
add("price_free","Free","免费","無料","무료","ฟรี","Gratis","Miễn phí","Gratis","Grátis")
add("price_free_tokens","5M tokens · Chinese","500万Token·国产","500万トークン·中国","500만 토큰·중국","5M โทเค็น·จีน","5M token·China","5M token·Trung Quốc","5M tokens·Chino","5M tokens·Chinês")
add("price_free_f1","All Chinese text models","全部国产文本模型","全中国テキストモデル","모든 중국 텍스트 모델","โมเดลข้อความจีนทั้งหมด","Semua model teks China","Tất cả mô hình văn bản Trung Quốc","Todos modelos de texto chinos","Todos modelos de texto chineses")
add("price_free_f2","5 requests/min","每分钟5请求","5リクエスト/分","분당 5요청","5 คำขอ/นาที","5 permintaan/menit","5 yêu cầu/phút","5 solicitudes/min","5 requisições/min")
add("price_free_f3","Auto Router included","含Auto Router","Auto Router付き","Auto Router 포함","รวม Auto Router","Termasuk Auto Router","Bao gồm Auto Router","Auto Router incluido","Auto Router incluso")
add("price_free_f4","Community support","社区支持","コミュニティサポート","커뮤니티 지원","สนับสนุนชุมชน","Dukungan komunitas","Hỗ trợ cộng đồng","Soporte comunitario","Suporte comunitário")
add("price_free_cta","Start Free","免费开始","無料で始める","무료 시작","เริ่มฟรี","Mulai Gratis","Bắt đầu miễn phí","Comenzar Gratis","Começar Grátis")

add("price_starter","Starter","Starter","Starter","Starter","Starter","Starter","Starter","Starter","Starter")
add("price_starter_tokens","50M tokens · All Chinese","5000万Token·全国产","5000万トークン·全中国","5000만 토큰·전체 중국","50M โทเค็น·จีนทั้งหมด","50M token·Semua China","50M token·Tất cả Trung Quốc","50M tokens·Todo chino","50M tokens·Tudo chinês")
add("price_starter_f1","All Chinese text models","全部国产文本模型","全中国テキストモデル","모든 중국 텍스트 모델","โมเดลข้อความจีนทั้งหมด","Semua model teks China","Tất cả mô hình văn bản Trung Quốc","Todos modelos de texto chinos","Todos modelos de texto chineses")
add("price_starter_f2","Unlimited requests","无限请求","無制限リクエスト","무제한 요청","คำขอไม่จำกัด","Permintaan tak terbatas","Yêu cầu không giới hạn","Solicitudes ilimitadas","Requisições ilimitadas")
add("price_starter_f3","Auto Router · 3 tiers","Auto Router · 3档","Auto Router · 3層","Auto Router · 3단계","Auto Router · 3 ระดับ","Auto Router · 3 tingkat","Auto Router · 3 tầng","Auto Router · 3 niveles","Auto Router · 3 níveis")
add("price_starter_f4","Email support","邮件支持","メールサポート","이메일 지원","สนับสนุนทางอีเมล","Dukungan email","Hỗ trợ email","Soporte por email","Suporte por email")
add("price_starter_f5","Usage dashboard","用量面板","使用量ダッシュボード","사용량 대시보드","แดชบอร์ดการใช้งาน","Dasbor penggunaan","Bảng điều khiển sử dụng","Panel de uso","Painel de uso")
add("price_starter_cta","Subscribe","订阅","購読","구독","สมัคร","Berlangganan","Đăng ký","Suscribirse","Assinar")

add("price_pro","Pro","Pro","Pro","Pro","Pro","Pro","Pro","Pro","Pro")
add("price_pro_tokens","200M tokens · Chinese","2亿Token·国产","2億トークン·中国","2억 토큰·중국","200M โทเค็น·จีน","200M token·China","200M token·Trung Quốc","200M tokens·Chino","200M tokens·Chinês")
add("price_pro_f1","Everything in Starter","Starter全部内容","Starterの全機能","Starter 모든 기능","ทุกอย่างใน Starter","Semua di Starter","Mọi thứ trong Starter","Todo en Starter","Tudo no Starter")
add("price_pro_f2","Priority routing","优先路由","優先ルーティング","우선 라우팅","เส้นทางลำดับความสำคัญ","Rute prioritas","Định tuyến ưu tiên","Enrutamiento prioritario","Roteamento prioritário")
add("price_pro_f3","Advanced analytics","高级分析","高度な分析","고급 분석","การวิเคราะห์ขั้นสูง","Analitik lanjutan","Phân tích nâng cao","Análisis avanzado","Análise avançada")
add("price_pro_cta","Go Pro","升级Pro","Proへ","Pro로","อัปเกรด Pro","Tingkatkan Pro","Nâng cấp Pro","Ir a Pro","Ir para Pro")

add("price_global","Global","Global","Global","Global","Global","Global","Global","Global","Global")
add("price_global_tokens","300M · Chinese + Intl","3亿·国产+国际","3億·中国+国際","3억·중국+국제","300M·จีน+นานาชาติ","300M·China+Intl","300M·Trung Quốc+Quốc tế","300M·Chino+Intl","300M·Chinês+Intl")
add("price_global_f1","Everything in Pro","Pro全部内容","Proの全機能","Pro 모든 기능","ทุกอย่างใน Pro","Semua di Pro","Mọi thứ trong Pro","Todo en Pro","Tudo no Pro")
add("price_global_f2","100M international models","1亿国际模型","1億国際モデル","1억 국제 모델","100M โมเดลนานาชาติ","100M model internasional","100M mô hình quốc tế","100M modelos internacionales","100M modelos internacionais")
add("price_global_f3","GPT-4o · Claude · Gemini","GPT-4o · Claude · Gemini","GPT-4o · Claude · Gemini","GPT-4o · Claude · Gemini","GPT-4o · Claude · Gemini","GPT-4o · Claude · Gemini","GPT-4o · Claude · Gemini","GPT-4o · Claude · Gemini","GPT-4o · Claude · Gemini")
add("price_global_f4","Global routing","全球路由","グローバルルーティング","글로벌 라우팅","เส้นทางทั่วโลก","Rute global","Định tuyến toàn cầu","Enrutamiento global","Roteamento global")
add("price_global_cta","Go Global","开启全球","グローバルへ","글로벌로","ไปทั่วโลก","Go Global","Đi Toàn cầu","Ir Global","Ir Global")

add("price_ent","Enterprise","Enterprise","Enterprise","Enterprise","Enterprise","Enterprise","Enterprise","Enterprise","Enterprise")
add("price_ent_desc","$299/mo · 2B tokens · Custom SLA","$299/月·20亿Token·定制SLA","$299/月·20億トークン·カスタムSLA","$299/월·20억 토큰·맞춤 SLA","$299/เดือน·2B โทเค็น·SLA กำหนดเอง","$299/bln·2B token·SLA kustom","$299/tháng·2B token·SLA tùy chỉnh","$299/mes·2B tokens·SLA personalizado","$299/mês·2B tokens·SLA personalizado")
add("price_ent_cta","Contact Sales","联系销售","営業に問い合わせ","영업팀 문의","ติดต่อฝ่ายขาย","Hubungi Sales","Liên hệ Kinh doanh","Contactar Ventas","Falar com Vendas")
add("pricing_label","Pricing","定价","料金","가격","ราคา","Harga","Giá","Precios","Preços")
add("pricing_title","Simple, transparent, competitive","简单、透明、有竞争力","シンプル、透明、競争力あり","간단하고 투명하며 경쟁력 있는","เรียบง่าย โปร่งใส แข่งขันได้","Sederhana, transparan, kompetitif","Đơn giản, minh bạch, cạnh tranh","Simple, transparente, competitivo","Simples, transparente, competitivo")
add("pricing_sub","All plans include OpenAI-compatible API + Auto Router. Pay only for what you use beyond included tokens.","所有套餐含OpenAI兼容API+Auto Router。超额按量计费。","全プランにOpenAI互換APIとAuto Routerが含まれます。含まれるトークンを超えた分のみお支払い。","모든 플랜에 OpenAI 호환 API + Auto Router 포함. 포함된 토큰 초과분만 지불.","ทุกแผนรวม API ที่เข้ากันได้กับ OpenAI + Auto Router จ่ายเฉพาะส่วนที่เกินโทเค็นที่รวมไว้","Semua paket termasuk API kompatibel OpenAI + Auto Router. Bayar hanya untuk penggunaan di luar token yang disertakan.","Tất cả gói bao gồm API tương thích OpenAI + Auto Router. Chỉ trả cho phần vượt quá token bao gồm.","Todos los planes incluyen API compatible con OpenAI + Auto Router. Paga solo por lo que uses más allá de los tokens incluidos.","Todos os planos incluem API compatível com OpenAI + Auto Router. Pague apenas pelo que usar além dos tokens incluídos.")

# Router
add("router_label","Competitive Edge","竞争优势","競争優位","경쟁 우위","ความได้เปรียบในการแข่งขัน","Keunggulan Kompetitif","Lợi thế cạnh tranh","Ventaja Competitiva","Vantagem Competitiva")
add("router_title","The only platform with Auto Intelligent Routing","唯一拥有Auto智能路由的平台","Autoインテリジェントルーティングを搭載した唯一のプラットフォーム","Auto 지능형 라우팅을 갖춘 유일한 플랫폼","แพลตฟอร์มเดียวที่มี Auto Intelligent Routing","Satu-satunya platform dengan Auto Intelligent Routing","Nền tảng duy nhất có Định tuyến Thông minh Tự động","La única plataforma con Auto Intelligent Routing","A única plataforma com Auto Intelligent Routing")
add("router_sub","OpenRouter doesn't have it. SiliconFlow doesn't have it. Qiniu doesn't have it. Only AICraft automatically selects the optimal model for every request.","OpenRouter没有。硅基流动没有。七牛云没有。只有AICraft自动为每个请求选择最优模型。","OpenRouterにはない。SiliconFlowにもない。Qiniuにもない。AICraftだけが各リクエストに最適なモデルを自動選択します。","OpenRouter에도, SiliconFlow에도, Qiniu에도 없습니다. AICraft만이 각 요청에 최적의 모델을 자동 선택합니다.","OpenRouter ไม่มี SiliconFlow ไม่มี Qiniu ไม่มี มีเพียง AICraft ที่เลือกโมเดลที่ดีที่สุดโดยอัตโนมัติสำหรับทุกคำขอ","OpenRouter tidak punya. SiliconFlow tidak punya. Qiniu tidak punya. Hanya AICraft yang otomatis memilih model optimal untuk setiap permintaan.","OpenRouter không có. SiliconFlow không có. Qiniu không có. Chỉ AICraft tự động chọn mô hình tối ưu cho mọi yêu cầu.","OpenRouter no lo tiene. SiliconFlow no lo tiene. Qiniu no lo tiene. Solo AICraft selecciona automáticamente el modelo óptimo.","OpenRouter não tem. SiliconFlow não tem. Qiniu não tem. Só a AICraft seleciona automaticamente o modelo ideal.")
add("router_stat1","6 Categories","6大分类","6カテゴリ","6개 카테고리","6 หมวดหมู่","6 Kategori","6 Danh mục","6 Categorías","6 Categorias")
add("router_stat1_sub","Auto task detection","自动任务检测","自動タスク検出","자동 작업 감지","ตรวจจับงานอัตโนมัติ","Deteksi tugas otomatis","Phát hiện tác vụ tự động","Detección automática de tareas","Detecção automática de tarefas")
add("router_stat2","0.3ms Overhead","0.3ms开销","0.3msオーバーヘッド","0.3ms 오버헤드","ค่าใช้จ่าย 0.3ms","Overhead 0.3ms","Chi phí 0.3ms","0.3ms de sobrecarga","0.3ms de overhead")
add("router_stat2_sub","$0.0000006 per call","每次$0.0000006","1回$0.0000006","호출당 $0.0000006","$0.0000006 ต่อคำขอ","$0.0000006 per panggilan","$0.0000006 mỗi lần gọi","$0.0000006 por llamada","$0.0000006 por chamada")
add("router_stat3","Auto Fallback","自动故障切换","自動フォールバック","자동 폴백","Fallback อัตโนมัติ","Fallback Otomatis","Dự phòng tự động","Fallback Automático","Fallback Automático")
add("router_stat3_sub","Primary fails → backup","主模型故障→备用","プライマリ失敗→バックアップ","주 모델 실패→백업","หลักล้มเหลว → สำรอง","Utama gagal → cadangan","Chính thất bại → dự phòng","Principal falla → respaldo","Principal falha → backup")
add("router_stat4","91% Avg Saving","平均节省91%","平均91%削減","평균 91% 절감","ประหยัดเฉลี่ย 91%","Rata-rata hemat 91%","Tiết kiệm trung bình 91%","91% Ahorro Promedio","91% Economia Média")
add("router_stat4_sub","vs GPT-4","对比GPT-4","GPT-4比","GPT-4 대비","เทียบ GPT-4","vs GPT-4","so với GPT-4","vs GPT-4","vs GPT-4")

# Router compare
add("router_good_title","With AICraft Auto Router","使用AICraft Auto Router","AICraft Auto Routerを使用","AICraft Auto Router 사용","ด้วย AICraft Auto Router","Dengan AICraft Auto Router","Với AICraft Auto Router","Con AICraft Auto Router","Com AICraft Auto Router")
add("router_bad_title","Without (like OpenRouter)","不使用（如OpenRouter）","なし（OpenRouterなど）","없이 (OpenRouter 등)","ไม่มี (เช่น OpenRouter)","Tanpa (seperti OpenRouter)","Không có (như OpenRouter)","Sin (como OpenRouter)","Sem (como OpenRouter)")

# Router table
add("rt_task","Task","任务","タスク","작업","งาน","Tugas","Tác vụ","Tarea","Tarefa")
add("rt_primary","Primary Model","首选模型","プライマリモデル","주 모델","โมเดลหลัก","Model Utama","Mô hình Chính","Modelo Principal","Modelo Primário")
add("rt_fallback","Fallback","备用","フォールバック","폴백","สำรอง","Cadangan","Dự phòng","Respaldo","Backup")
add("rt_budget","Budget Pick","省钱选择","予算向け","예산 선택","ตัวเลือกประหยัด","Pilihan Hemat","Lựa chọn Tiết kiệm","Opción Económica","Opção Econômica")
add("rt_save","vs GPT-4","对比GPT-4","GPT-4比","GPT-4 대비","เทียบ GPT-4","vs GPT-4","so với GPT-4","vs GPT-4","vs GPT-4")
add("rt_coding","Coding","编程","コーディング","코딩","การเขียนโค้ด","Coding","Lập trình","Programación","Programação")
add("rt_translation","Translation/Batch","翻译/批量","翻訳/バッチ","번역/배치","แปล/ชุด","Terjemahan/Batch","Dịch/Hàng loạt","Traducción/Lote","Tradução/Lote")
add("rt_chinese","Chinese/Multilingual","中文/多语言","中国語/多言語","중국어/다국어","จีน/หลายภาษา","China/Multibahasa","Tiếng Trung/Đa ngôn ngữ","Chino/Multilingüe","Chinês/Multilíngue")
add("rt_reasoning","Reasoning/Logic","推理/逻辑","推論/論理","추론/논리","การใช้เหตุผล/ตรรกะ","Penalaran/Logika","Suy luận/Logic","Razonamiento/Lógica","Raciocínio/Lógica")
add("rt_creative","Creative Writing","创意写作","クリエイティブライティング","창의적 글쓰기","การเขียนสร้างสรรค์","Menulis Kreatif","Viết Sáng tạo","Escritura Creativa","Escrita Criativa")
add("rt_chat","Customer Service","客服对话","カスタマーサービス","고객 서비스","บริการลูกค้า","Layanan Pelanggan","Dịch vụ Khách hàng","Servicio al Cliente","Atendimento ao Cliente")

# Docs
add("docs_label","Quick Start","快速开始","クイックスタート","빠른 시작","เริ่มต้นอย่างรวดเร็ว","Mulai Cepat","Bắt đầu Nhanh","Inicio Rápido","Início Rápido")
add("docs_title","3 lines to integrate","三行代码接入","3行で統合","3줄로 통합","3 บรรทัดเพื่อผสานรวม","3 baris untuk integrasi","3 dòng để tích hợp","3 líneas para integrar","3 linhas para integrar")
add("docs_sub","Drop-in replacement for OpenAI. Works with Python, Node, Go, Rust, curl — any HTTP client.","OpenAI直接替换。支持Python、Node、Go、Rust、curl——任何HTTP客户端。","OpenAIの代替として。Python、Node、Go、Rust、curlで動作。","OpenAI 대체. Python, Node, Go, Rust, curl 지원.","แทนที่ OpenAI โดยตรง ทำงานกับ Python, Node, Go, Rust, curl — ไคลเอนต์ HTTP ใดๆ","Pengganti langsung OpenAI. Bekerja dengan Python, Node, Go, Rust, curl.","Thay thế trực tiếp OpenAI. Hoạt động với Python, Node, Go, Rust, curl.","Reemplazo directo de OpenAI. Funciona con Python, Node, Go, Rust, curl.","Substituto direto do OpenAI. Funciona com Python, Node, Go, Rust, curl.")

# Privacy
add("privacy_label","Trust & Compliance","信任与合规","信頼とコンプライアンス","신뢰와 규정 준수","ความไว้วางใจและการปฏิบัติตาม","Kepercayaan & Kepatuhan","Tin cậy & Tuân thủ","Confianza y Cumplimiento","Confiança e Conformidade")
add("privacy_title","Privacy by jurisdiction","按司法管辖区保护隐私","管轄区域ごとのプライバシー","관할권별 개인정보 보호","ความเป็นส่วนตัวตามเขตอำนาจ","Privasi berdasarkan yurisdiksi","Quyền riêng tư theo khu vực pháp lý","Privacidad por jurisdicción","Privacidade por jurisdição")
add("privacy_sub","GDPR (EU) · PIPL (China) · LGPD (Brazil) · CCPA (California)","GDPR（欧盟）· PIPL（中国）· LGPD（巴西）· CCPA（加州）","GDPR（EU）· PIPL（中国）· LGPD（ブラジル）· CCPA（カリフォルニア）","GDPR (EU) · PIPL (중국) · LGPD (브라질) · CCPA (캘리포니아)","GDPR (EU) · PIPL (จีน) · LGPD (บราซิล) · CCPA (แคลิฟอร์เนีย)","GDPR (EU) · PIPL (China) · LGPD (Brasil) · CCPA (California)","GDPR (EU) · PIPL (Trung Quốc) · LGPD (Brazil) · CCPA (California)","GDPR (UE) · PIPL (China) · LGPD (Brasil) · CCPA (California)","GDPR (UE) · PIPL (China) · LGPD (Brasil) · CCPA (Califórnia)")
add("privacy_data_title","Data Commitments","数据承诺","データコミットメント","데이터 약속","พันธสัญญาข้อมูล","Komitmen Data","Cam kết Dữ liệu","Compromisos de Datos","Compromissos de Dados")
add("privacy_d1","No conversation content stored","不存储对话内容","会話内容を保存しません","대화 내용 저장하지 않음","ไม่จัดเก็บเนื้อหาการสนทนา","Tidak menyimpan konten percakapan","Không lưu trữ nội dung hội thoại","Sin almacenamiento de conversaciones","Sem armazenamento de conversas")
add("privacy_d2","TLS 1.3 encryption end-to-end","TLS 1.3端到端加密","TLS 1.3エンドツーエンド暗号化","TLS 1.3 종단간 암호화","การเข้ารหัส TLS 1.3 แบบ end-to-end","Enkripsi TLS 1.3 end-to-end","Mã hóa TLS 1.3 end-to-end","Cifrado TLS 1.3 de extremo a extremo","Criptografia TLS 1.3 ponta a ponta")
add("privacy_d3","API keys cryptographically hashed","API密钥哈希存储","APIキーを暗号化ハッシュで保存","API 키 암호화 해시 저장","คีย์ API ถูกแฮชด้วยการเข้ารหัส","Kunci API di-hash secara kriptografis","Khóa API được băm mật mã","Claves API con hash criptográfico","Chaves API com hash criptográfico")
add("privacy_d4","Chinese model data stays in China","国产模型数据不出境","中国モデルのデータは中国国内に","중국 모델 데이터는 중국 내 유지","ข้อมูลโมเดลจีนอยู่ในจีน","Data model China tetap di China","Dữ liệu mô hình Trung Quốc ở trong Trung Quốc","Datos de modelos chinos permanecen en China","Dados de modelos chineses permanecem na China")
add("privacy_d5","International via Hetao data bubble","国际模型经河套数据气泡","国際モデルは河套データバブル経由","국제 모델은 Hetao 데이터 버블 경유","ระหว่างประเทศผ่าน Hetao data bubble","Internasional via Hetao data bubble","Quốc tế qua bong bóng dữ liệu Hetao","Internacional vía burbuja de datos Hetao","Internacional via bolha de dados Hetao")
add("privacy_d6","30-day max log retention","日志最多保留30天","ログ保持は最大30日","로그 최대 30일 보관","เก็บบันทึกสูงสุด 30 วัน","Retensi log maks 30 hari","Lưu nhật ký tối đa 30 ngày","Retención máxima de registros 30 días","Retenção máxima de logs 30 dias")

# GDPR card
add("privacy_gdpr_title","GDPR (EU/EEA)","GDPR（欧盟/欧洲经济区）","GDPR（EU/EEA）","GDPR (EU/EEA)","GDPR (EU/EEA)","GDPR (EU/EEA)","GDPR (EU/EEA)","GDPR (UE/EEE)","GDPR (UE/EEE)")
add("privacy_gdpr_l1","AICraft as Data Processor","AICraft作为数据处理者","AICraftがデータ処理者として","AICraft가 데이터 처리자로","AICraft เป็นผู้ประมวลผลข้อมูล","AICraft sebagai Pemroses Data","AICraft là Bộ xử lý Dữ liệu","AICraft como Procesador de Datos","AICraft como Processador de Dados")
add("privacy_gdpr_l2","SCCs for cross-border transfers","SCC跨境传输协议","SCCsによる越境転送","SCCs로 국경 간 전송","SCCs สำหรับการโอนข้ามพรมแดน","SCCs untuk transfer lintas batas","SCCs cho chuyển giao xuyên biên giới","SCCs para transferencias transfronterizas","SCCs para transferências transfronteiriças")
add("privacy_gdpr_l3","Right to erasure (30 days)","删除权（30天内）","消去権（30日以内）","삭제 권리 (30일 이내)","สิทธิ์ในการลบ (30 วัน)","Hak untuk menghapus (30 hari)","Quyền xóa (30 ngày)","Derecho al borrado (30 días)","Direito ao apagamento (30 dias)")
add("privacy_gdpr_l4","DPO: dpo@aicraftapi.com","数据保护官：dpo@aicraftapi.com","DPO: dpo@aicraftapi.com","DPO: dpo@aicraftapi.com","DPO: dpo@aicraftapi.com","DPO: dpo@aicraftapi.com","DPO: dpo@aicraftapi.com","DPO: dpo@aicraftapi.com","DPO: dpo@aicraftapi.com")

# PIPL card
add("privacy_pipl_title","PIPL (China)","PIPL（中国）","PIPL（中国）","PIPL (중국)","PIPL (จีน)","PIPL (China)","PIPL (Trung Quốc)","PIPL (China)","PIPL (China)")
add("privacy_pipl_l1","受托处理者：AICraft","受托处理者：AICraft","委託処理者：AICraft","수탁 처리자: AICraft","ผู้ประมวลผล: AICraft","Pemroses: AICraft","Bộ xử lý: AICraft","Procesador: AICraft","Processador: AICraft")
add("privacy_pipl_l2","法律依据：合同必需+知情同意","法律依据：合同必需+知情同意","法的根拠：契約上の必要性+同意","법적 근거: 계약 필요+동의","พื้นฐานทางกฎหมาย: ความจำเป็นตามสัญญา+ความยินยอม","Dasar hukum: Keperluan kontrak+persetujuan","Cơ sở pháp lý: Cần thiết hợp đồng+đồng ý","Base legal: Necesidad contractual+consentimiento","Base legal: Necessidade contratual+consentimento")
add("privacy_pipl_l3","数据跨境：河套数据气泡","数据跨境：河套数据气泡","越境データ：河套データバブル","국경 간 데이터: Hetao 데이터 버블","ข้อมูลข้ามพรมแดน: Hetao data bubble","Data lintas batas: Hetao data bubble","Dữ liệu xuyên biên giới: Bong bóng dữ liệu Hetao","Datos transfronterizos: Burbuja de datos Hetao","Dados transfronteiriços: Bolha de dados Hetao")
add("privacy_pipl_l4","联系：dpo@aicraftapi.com","联系：dpo@aicraftapi.com","連絡先：dpo@aicraftapi.com","연락처: dpo@aicraftapi.com","ติดต่อ: dpo@aicraftapi.com","Kontak: dpo@aicraftapi.com","Liên hệ: dpo@aicraftapi.com","Contacto: dpo@aicraftapi.com","Contato: dpo@aicraftapi.com")

# LGPD+CCPA card
add("privacy_other_title","LGPD · CCPA","LGPD · CCPA","LGPD · CCPA","LGPD · CCPA","LGPD · CCPA","LGPD · CCPA","LGPD · CCPA","LGPD · CCPA","LGPD · CCPA")
add("privacy_other_l1","LGPD: Operador de dados · SCCs","LGPD：数据操作者 · SCCs","LGPD：データオペレーター · SCCs","LGPD: 데이터 운영자 · SCCs","LGPD: ผู้ดำเนินการข้อมูล · SCCs","LGPD: Operator data · SCCs","LGPD: Nhà điều hành dữ liệu · SCCs","LGPD: Operador de datos · SCCs","LGPD: Operador de dados · SCCs")
add("privacy_other_l2","CCPA: We do NOT sell personal data","CCPA：我们不出售个人数据","CCPA：個人データを販売しません","CCPA: 개인 데이터 판매하지 않음","CCPA: เราไม่ขายข้อมูลส่วนบุคคล","CCPA: Kami TIDAK menjual data pribadi","CCPA: Chúng tôi KHÔNG bán dữ liệu cá nhân","CCPA: NO vendemos datos personales","CCPA: NÃO vendemos dados pessoais")
add("privacy_other_l3","Right to know · Right to delete","知情权 · 删除权","知る権利 · 削除する権利","알 권리 · 삭제할 권리","สิทธิ์ในการรู้ · สิทธิ์ในการลบ","Hak untuk tahu · Hak untuk menghapus","Quyền được biết · Quyền xóa","Derecho a saber · Derecho a eliminar","Direito de saber · Direito de excluir")
add("privacy_other_l4","privacy@aicraftapi.com","privacy@aicraftapi.com","privacy@aicraftapi.com","privacy@aicraftapi.com","privacy@aicraftapi.com","privacy@aicraftapi.com","privacy@aicraftapi.com","privacy@aicraftapi.com","privacy@aicraftapi.com")

# Consent
add("consent_label","I agree to Privacy Policy & Terms of Service. I understand API requests are routed to upstream model providers. International model traffic may transit through OpenRouter (USA).","我同意隐私政策和服务条款。我理解API请求会路由到上游模型提供商。国际模型流量可能经由OpenRouter（美国）传输。","プライバシーポリシーと利用規約に同意します。APIリクエストが上流のモデルプロバイダーにルーティングされることを理解しています。国際モデルのトラフィックはOpenRouter（米国）を経由する場合があります。","개인정보 처리방침 및 이용약관에 동의합니다. API 요청이 업스트림 모델 제공업체로 라우팅됨을 이해합니다. 국제 모델 트래픽은 OpenRouter(미국)를 경유할 수 있습니다.","ฉันยอมรับนโยบายความเป็นส่วนตัวและข้อกำหนดในการให้บริการ ฉันเข้าใจว่าคำขอ API ถูกส่งไปยังผู้ให้บริการโมเดลต้นทาง การรับส่งข้อมูลโมเดลระหว่างประเทศอาจผ่าน OpenRouter (สหรัฐอเมริกา)","Saya menyetujui Kebijakan Privasi & Ketentuan Layanan. Saya memahami permintaan API dirutekan ke penyedia model upstream. Lalu lintas model internasional dapat melalui OpenRouter (AS).","Tôi đồng ý với Chính sách Quyền riêng tư & Điều khoản Dịch vụ. Tôi hiểu các yêu cầu API được định tuyến đến nhà cung cấp mô hình thượng nguồn. Lưu lượng mô hình quốc tế có thể qua OpenRouter (Hoa Kỳ).","Acepto la Política de Privacidad y los Términos de Servicio. Entiendo que las solicitudes API se enrutan a proveedores de modelos upstream. El tráfico de modelos internacionales puede pasar por OpenRouter (EE.UU.).","Concordo com a Política de Privacidade e Termos de Serviço. Entendo que as solicitações API são roteadas para provedores de modelo upstream. O tráfego de modelos internacionais pode passar pelo OpenRouter (EUA).")

# Signup modal
add("signup_title","Create your AICraft account","创建AICraft账户","AICraftアカウントを作成","AICraft 계정 만들기","สร้างบัญชี AICraft","Buat akun AICraft Anda","Tạo tài khoản AICraft","Crea tu cuenta AICraft","Crie sua conta AICraft")
add("signup_sub","Free to start. No credit card required.","免费开始。无需信用卡。","無料で始められます。クレジットカード不要。","무료 시작. 신용카드 불필요.","เริ่มต้นฟรี ไม่ต้องใช้บัตรเครดิต","Gratis untuk memulai. Tanpa kartu kredit.","Miễn phí bắt đầu. Không cần thẻ tín dụng.","Gratis para empezar. Sin tarjeta de crédito.","Grátis para começar. Sem cartão de crédito.")
add("signup_email","Email","邮箱","メール","이메일","อีเมล","Email","Email","Correo electrónico","Email")
add("signup_email_ph","you@example.com","you@example.com","you@example.com","you@example.com","you@example.com","you@example.com","you@example.com","tu@ejemplo.com","voce@exemplo.com")
add("signup_password","Password","密码","パスワード","비밀번호","รหัสผ่าน","Kata Sandi","Mật khẩu","Contraseña","Senha")
add("signup_password_ph","Min 8 characters","至少8个字符","8文字以上","최소 8자","อย่างน้อย 8 ตัวอักษร","Min 8 karakter","Ít nhất 8 ký tự","Mín 8 caracteres","Mín 8 caracteres")
add("signup_name","Full Name","全名","氏名","전체 이름","ชื่อเต็ม","Nama Lengkap","Họ và tên","Nombre Completo","Nome Completo")
add("signup_name_ph","Your name","你的名字","あなたの名前","당신의 이름","ชื่อของคุณ","Nama Anda","Tên của bạn","Tu nombre","Seu nome")
add("signup_country","Country / Region","国家/地区","国/地域","국가/지역","ประเทศ/ภูมิภาค","Negara/Wilayah","Quốc gia/Khu vực","País/Región","País/Região")
add("signup_country_select","Select...","请选择...","選択...","선택...","เลือก...","Pilih...","Chọn...","Seleccionar...","Selecionar...")
add("signup_usecase","How will you use AICraft?","你将如何使用AICraft？","AICraftをどのように使用しますか？","AICraft를 어떻게 사용하시겠습니까?","คุณจะใช้ AICraft อย่างไร?","Bagaimana Anda akan menggunakan AICraft?","Bạn sẽ sử dụng AICraft như thế nào?","¿Cómo usarás AICraft?","Como você usará o AICraft?")
add("signup_usecase_select","Select...","请选择...","選択...","선택...","เลือก...","Pilih...","Chọn...","Seleccionar...","Selecionar...")
add("signup_usecase_1","Personal project / Hobby","个人项目/爱好","個人プロジェクト/趣味","개인 프로젝트/취미","โปรเจกต์ส่วนตัว/งานอดิเรก","Proyek pribadi/Hobi","Dự án cá nhân/Sở thích","Proyecto personal/Hobby","Projeto pessoal/Hobby")
add("signup_usecase_2","Startup / Small business","创业/小企业","スタートアップ/中小企業","스타트업/소기업","สตาร์ทอัพ/ธุรกิจขนาดเล็ก","Startup/Usaha kecil","Khởi nghiệp/Doanh nghiệp nhỏ","Startup/Pequeña empresa","Startup/Pequena empresa")
add("signup_usecase_3","Enterprise / Company","企业/公司","エンタープライズ/企業","엔터프라이즈/회사","องค์กร/บริษัท","Enterprise/Perusahaan","Doanh nghiệp/Công ty","Empresa/Compañía","Empresa/Companhia")
add("signup_usecase_4","Academic / Research","学术/研究","学術/研究","학술/연구","วิชาการ/วิจัย","Akademik/Penelitian","Học thuật/Nghiên cứu","Académico/Investigación","Acadêmico/Pesquisa")
add("signup_usecase_5","Just exploring / Learning","探索/学习","探索/学習","탐색/학습","สำรวจ/เรียนรู้","Menjelajah/Belajar","Khám phá/Học tập","Explorando/Aprendiendo","Explorando/Aprendendo")
add("signup_source","How did you hear about us?","你从哪里了解到我们？","どこで私たちを知りましたか？","어디서 저희를 알게 되셨나요?","คุณรู้จักเราจากที่ไหน?","Bagaimana Anda tahu tentang kami?","Bạn biết đến chúng tôi từ đâu?","¿Cómo nos conociste?","Como você nos conheceu?")
add("signup_source_select","Select (optional)","请选择（选填）","選択（任意）","선택 (선택사항)","เลือก (ไม่บังคับ)","Pilih (opsional)","Chọn (tùy chọn)","Seleccionar (opcional)","Selecionar (opcional)")
add("signup_source_1","GitHub","GitHub","GitHub","GitHub","GitHub","GitHub","GitHub","GitHub","GitHub")
add("signup_source_2","Google Search","Google搜索","Google検索","Google 검색","Google Search","Google Search","Tìm kiếm Google","Búsqueda de Google","Pesquisa Google")
add("signup_source_3","Dev.to / Hashnode","Dev.to / Hashnode","Dev.to / Hashnode","Dev.to / Hashnode","Dev.to / Hashnode","Dev.to / Hashnode","Dev.to / Hashnode","Dev.to / Hashnode","Dev.to / Hashnode")
add("signup_source_4","Reddit / Hacker News","Reddit / Hacker News","Reddit / Hacker News","Reddit / Hacker News","Reddit / Hacker News","Reddit / Hacker News","Reddit / Hacker News","Reddit / Hacker News","Reddit / Hacker News")
add("signup_source_5","Friend / Colleague","朋友/同事","友人/同僚","친구/동료","เพื่อน/เพื่อนร่วมงาน","Teman/Kolega","Bạn bè/Đồng nghiệp","Amigo/Colega","Amigo/Colega")
add("signup_source_6","Social Media","社交媒体","ソーシャルメディア","소셜 미디어","โซเชียลมีเดีย","Media Sosial","Mạng xã hội","Redes Sociales","Redes Sociais")
add("signup_consent_privacy","I agree to the Privacy Policy and consent to data processing.","我同意隐私政策并同意数据处理。","プライバシーポリシーに同意し、データ処理に同意します。","개인정보 처리방침에 동의하고 데이터 처리에 동의합니다.","ฉันยอมรับนโยบายความเป็นส่วนตัวและยินยอมให้ประมวลผลข้อมูล","Saya menyetujui Kebijakan Privasi dan menyetujui pemrosesan data.","Tôi đồng ý với Chính sách Quyền riêng tư và đồng ý xử lý dữ liệu.","Acepto la Política de Privacidad y consiento el procesamiento de datos.","Concordo com a Política de Privacidade e consinto com o processamento de dados.")
add("signup_consent_terms","I agree to the Terms of Service.","我同意服务条款。","利用規約に同意します。","이용약관에 동의합니다.","ฉันยอมรับข้อกำหนดในการให้บริการ","Saya menyetujui Ketentuan Layanan.","Tôi đồng ý với Điều khoản Dịch vụ.","Acepto los Términos de Servicio.","Concordo com os Termos de Serviço.")
add("signup_consent_crossborder","I understand international model requests may transit through OpenRouter (USA).","我理解国际模型请求可能经由OpenRouter（美国）传输。","国際モデルのリクエストがOpenRouter（米国）を経由する可能性があることを理解しています。","국제 모델 요청이 OpenRouter(미국)를 경유할 수 있음을 이해합니다.","ฉันเข้าใจว่าคำขอโมเดลระหว่างประเทศอาจผ่าน OpenRouter (สหรัฐอเมริกา)","Saya memahami permintaan model internasional dapat melalui OpenRouter (AS).","Tôi hiểu các yêu cầu mô hình quốc tế có thể qua OpenRouter (Hoa Kỳ).","Entiendo que las solicitudes de modelos internacionales pueden pasar por OpenRouter (EE.UU.).","Entendo que as solicitações de modelos internacionais podem passar pelo OpenRouter (EUA).")
add("signup_submit","Create Account","创建账户","アカウントを作成","계정 만들기","สร้างบัญชี","Buat Akun","Tạo Tài khoản","Crear Cuenta","Criar Conta")
add("signup_login","Already have an account?","已有账户？","すでにアカウントをお持ちですか？","이미 계정이 있으신가요?","มีบัญชีอยู่แล้ว?","Sudah punya akun?","Đã có tài khoản?","¿Ya tienes cuenta?","Já tem conta?")
add("signup_login_link","Sign in","登录","サインイン","로그인","เข้าสู่ระบบ","Masuk","Đăng nhập","Iniciar sesión","Entrar")

# Chat
add("chat_header","AICraft Assistant · AI-Powered","AICraft助手·AI驱动","AICraftアシスタント·AI搭載","AICraft 어시스턴트·AI 구동","AICraft ผู้ช่วย·ขับเคลื่อนด้วย AI","AICraft Asisten·Didukung AI","AICraft Trợ lý·Hỗ trợ AI","AICraft Asistente·Impulsado por IA","AICraft Assistente·Impulsionado por IA")
add("chat_placeholder","Ask me anything...","问我任何问题...","何でも聞いてください...","무엇이든 물어보세요...","ถามอะไรก็ได้...","Tanya apa saja...","Hỏi tôi bất cứ điều gì...","Pregúntame cualquier cosa...","Pergunte qualquer coisa...")
add("chat_greeting","Hi! Ask me anything about AICraft API, pricing, or getting started.","你好！问我任何关于AICraft API、定价或如何开始的问题。","こんにちは！AICraft API、料金、始め方について何でも聞いてください。","안녕하세요! AICraft API, 가격, 시작하기에 대해 무엇이든 물어보세요.","สวัสดี! ถามฉันเกี่ยวกับ AICraft API, ราคา, หรือวิธีการเริ่มต้น","Hai! Tanya saya tentang AICraft API, harga, atau cara memulai.","Xin chào! Hỏi tôi về AICraft API, giá cả, hoặc cách bắt đầu.","¡Hola! Pregúntame sobre AICraft API, precios o cómo empezar.","Olá! Pergunte-me sobre AICraft API, preços ou como começar.")
add("chat_powered","Powered by AICraft Auto Router","由AICraft Auto Router驱动","AICraft Auto Router搭載","AICraft Auto Router 구동","ขับเคลื่อนโดย AICraft Auto Router","Didukung oleh AICraft Auto Router","Được hỗ trợ bởi AICraft Auto Router","Impulsado por AICraft Auto Router","Impulsionado pelo AICraft Auto Router")

# Footer
add("footer_product","Product","产品","製品","제품","ผลิตภัณฑ์","Produk","Sản phẩm","Producto","Produto")
add("footer_company","Company","公司","会社","회사","บริษัท","Perusahaan","Công ty","Empresa","Empresa")
add("footer_legal","Legal","法律","法的情報","법적 정보","กฎหมาย","Hukum","Pháp lý","Legal","Jurídico")
add("footer_api","API","API","API","API","API","API","API","API","API")
add("footer_models","Models","模型","モデル","모델","โมเดล","Model","Mô hình","Modelos","Modelos")
add("footer_pricing","Pricing","定价","料金","가격","ราคา","Harga","Giá","Precios","Preços")
add("footer_router","Auto Router","智能路由","自動ルート","자동 라우팅","เส้นทางอัตโนมัติ","Rute Otomatis","Định tuyến tự động","Auto Router","Auto Router")
add("footer_about","About","关于","会社概要","소개","เกี่ยวกับ","Tentang","Giới thiệu","Acerca de","Sobre")
add("footer_blog","Blog","博客","ブログ","블로그","บล็อก","Blog","Blog","Blog","Blog")
add("footer_careers","Careers","招聘","採用","채용","ร่วมงาน","Karir","Nghề nghiệp","Carreras","Carreiras")
add("footer_contact","Contact","联系","お問い合わせ","연락처","ติดต่อ","Kontak","Liên hệ","Contacto","Contato")
add("footer_privacy","Privacy Policy","隐私政策","プライバシーポリシー","개인정보 처리방침","นโยบายความเป็นส่วนตัว","Kebijakan Privasi","Chính sách Quyền riêng tư","Política de Privacidad","Política de Privacidade")
add("footer_terms","Terms of Service","服务条款","利用規約","이용약관","ข้อกำหนดการให้บริการ","Ketentuan Layanan","Điều khoản Dịch vụ","Términos de Servicio","Termos de Serviço")
add("footer_dpa","DPA","DPA","DPA","DPA","DPA","DPA","DPA","DPA","DPA")
add("footer_sla","SLA","SLA","SLA","SLA","SLA","SLA","SLA","SLA","SLA")
add("footer_status","Status","状态","ステータス","상태","สถานะ","Status","Trạng thái","Estado","Status")
add("footer_github","GitHub","GitHub","GitHub","GitHub","GitHub","GitHub","GitHub","GitHub","GitHub")
add("footer_changelog","Changelog","更新日志","変更履歴","변경 로그","บันทึกการเปลี่ยนแปลง","Changelog","Nhật ký thay đổi","Registro de cambios","Registro de alterações")
add("footer_copyright","© 2026 AICraft · Shenzhen AICreatrix Technology Co., Ltd. · Hetao SZ-HK STIC Zone · aicraftapi.com","© 2026 AICraft · 深圳艾创矩阵科技有限公司 · 河套深港科技创新合作区 · aicraftapi.com","© 2026 AICraft · 深圳AICreatrix Technology Co., Ltd. · 河套SZ-HK STIC Zone · aicraftapi.com","© 2026 AICraft · Shenzhen AICreatrix Technology Co., Ltd. · Hetao SZ-HK STIC Zone · aicraftapi.com","© 2026 AICraft · Shenzhen AICreatrix Technology Co., Ltd. · Hetao SZ-HK STIC Zone · aicraftapi.com","© 2026 AICraft · Shenzhen AICreatrix Technology Co., Ltd. · Hetao SZ-HK STIC Zone · aicraftapi.com","© 2026 AICraft · Shenzhen AICreatrix Technology Co., Ltd. · Hetao SZ-HK STIC Zone · aicraftapi.com","© 2026 AICraft · Shenzhen AICreatrix Technology Co., Ltd. · Hetao SZ-HK STIC Zone · aicraftapi.com","© 2026 AICraft · Shenzhen AICreatrix Technology Co., Ltd. · Hetao SZ-HK STIC Zone · aicraftapi.com")

# ========== GENERATE HTML ==========
keys = list(T["en"].keys())
print(f"Total i18n keys: {len(keys)}")
print("Generating HTML...")

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=5.0">
<title>AICraft — Unified AI API · Auto Routing · 40+ Models</title>
<style>
:root{--bg:#f9fafb;--surface:#fff;--border:#e5e7eb;--border-light:#f3f4f6;--gold:#b8860b;--gold-light:rgba(184,134,11,0.08);--gold-glow:rgba(184,134,11,0.2);--text:#111827;--text2:#6b7280;--text3:#9ca3af;--blue:#2563eb;--green:#10b981;--red:#ef4444;--purple:#7c3aed;--radius:12px;--shadow-sm:0 1px 3px rgba(0,0,0,0.06);--shadow:0 4px 16px rgba(0,0,0,0.06);--shadow-lg:0 12px 40px rgba(0,0,0,0.1);--max-w:1120px}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:system-ui,-apple-system,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;overflow-x:hidden}
.nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.95);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:var(--max-w);margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:56px}
.nav-logo{display:flex;align-items:center;gap:8px;font-weight:800;font-size:18px;text-decoration:none;color:var(--text)}
.nav-logo b{display:flex;align-items:center;justify-content:center;width:32px;height:32px;background:linear-gradient(135deg,#b8860b,#d4a030);color:#fff;border-radius:8px;font-size:16px}
.nav-links{display:flex;gap:6px;align-items:center}
.nav-links a{color:var(--text2);text-decoration:none;font-size:13px;font-weight:500;padding:6px 12px;border-radius:6px;transition:all 0.15s}
.nav-links a:hover{color:var(--text);background:var(--bg)}
.nav-r{display:flex;gap:8px;align-items:center}
.nav-cta{padding:7px 16px;border-radius:20px;font-size:13px;font-weight:600;border:none;cursor:pointer;background:linear-gradient(135deg,#b8860b,#9a6d0c);color:#fff;transition:all 0.2s;white-space:nowrap}
.nav-cta:hover{box-shadow:0 4px 16px var(--gold-glow)}
.hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:10px;background:none;border:none}
.hamburger span{display:block;width:22px;height:2px;background:var(--text);border-radius:2px;transition:all 0.2s}
.mobile-menu{display:none;position:fixed;top:56px;left:0;width:100%;background:var(--surface);border-bottom:1px solid var(--border);z-index:99;padding:12px 20px;flex-direction:column;gap:4px;box-shadow:var(--shadow-lg)}
.mobile-menu.open{display:flex}
.mobile-menu a{padding:12px 16px;border-radius:8px;color:var(--text);text-decoration:none;font-size:15px;font-weight:500}
.sec{padding:70px 20px}.sec-inner{max-width:var(--max-w);margin:0 auto}
.sec-label{text-align:center;font-size:11px;text-transform:uppercase;letter-spacing:2px;color:var(--gold);font-weight:700;margin-bottom:8px}
.sec-title{text-align:center;font-size:clamp(22px,4vw,34px);font-weight:700;letter-spacing:-0.5px;margin-bottom:8px}
.sec-sub{text-align:center;color:var(--text2);max-width:520px;margin:0 auto;font-size:15px}
.hero{padding:80px 20px 60px;text-align:center;max-width:var(--max-w);margin:0 auto}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);padding:5px 14px;border-radius:20px;font-size:12px;color:var(--green);font-weight:600;margin-bottom:20px}
.hero-badge .dot{width:7px;height:7px;background:var(--green);border-radius:50%;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
.hero h1{font-size:clamp(28px,5vw,50px);font-weight:800;line-height:1.12;letter-spacing:-1px}
.hero h1 em{font-style:normal;background:linear-gradient(135deg,#b8860b,#d4a030);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{color:var(--text2);font-size:16px;max-width:560px;margin:16px auto 28px}
.hero-actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:6px;padding:11px 24px;border-radius:24px;font-size:14px;font-weight:600;cursor:pointer;text-decoration:none;transition:all 0.2s;border:none}
.btn-primary{background:linear-gradient(135deg,#b8860b,#9a6d0c);color:#fff;box-shadow:0 4px 14px var(--gold-glow)}
.btn-primary:hover{transform:translateY(-1px)}
.btn-outline{background:var(--surface);border:2px solid var(--border);color:var(--text)}
.btn-outline:hover{border-color:var(--gold)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px;box-shadow:var(--shadow-sm);transition:all 0.2s}
.card:hover{border-color:#d1d5db;box-shadow:var(--shadow)}
.model-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
.mc{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;box-shadow:var(--shadow-sm);transition:all 0.2s}
.mc:hover{border-color:var(--gold);box-shadow:var(--shadow)}
.mc-top{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.mc-av{width:30px;height:30px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:12px;color:#fff;font-weight:700;flex-shrink:0}
.mc-n{font-weight:600;font-size:13px;line-height:1.2}.mc-p{font-size:10px;color:var(--text3)}
.mc-d{font-size:11px;color:var(--text2);margin-bottom:8px;line-height:1.5;min-height:32px}
.mc-tags{display:flex;gap:4px;flex-wrap:wrap}
.tag{font-size:10px;font-weight:600;padding:2px 7px;border-radius:4px;background:var(--bg);color:var(--text2)}
.tag.grn{background:rgba(16,185,129,0.1);color:var(--green)}.tag.blu{background:rgba(37,99,235,0.08);color:var(--blue)}.tag.gld{background:rgba(184,134,11,0.08);color:var(--gold)}
.tabs{display:flex;gap:6px;justify-content:center;margin-bottom:30px;flex-wrap:wrap}
.tab-btn{padding:8px 18px;border-radius:20px;border:1.5px solid var(--border);background:var(--surface);color:var(--text2);font-size:12px;font-weight:500;cursor:pointer;transition:all 0.15s}
.tab-btn.active{background:var(--gold);color:#fff;border-color:var(--gold)}
.tab-panel{display:none}.tab-panel.active{display:block}
.pricing-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;align-items:start}
.pc{background:var(--surface);border:2px solid var(--border);border-radius:var(--radius);padding:24px 18px;text-align:center;box-shadow:var(--shadow-sm);position:relative}
.pc.pop{border-color:var(--gold);box-shadow:0 8px 32px var(--gold-glow)}
.pc.pop::before{content:'BEST VALUE';position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:var(--gold);color:#fff;font-size:9px;font-weight:700;padding:3px 12px;border-radius:10px;letter-spacing:1px}
.pc.glb{border-color:var(--blue);box-shadow:0 8px 32px rgba(37,99,235,0.15)}
.pc.glb::before{content:'GLOBAL';position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:var(--blue);color:#fff;font-size:9px;font-weight:700;padding:3px 12px;border-radius:10px}
.pc-name{font-weight:700;font-size:15px}.pc-amt{font-size:34px;font-weight:800;margin:10px 0 4px;letter-spacing:-1px}
.pc-amt small{font-size:13px;font-weight:400;color:var(--text3)}.pc-tok{font-size:11px;color:var(--text2);margin-bottom:14px}
.pc-feat{list-style:none;text-align:left;font-size:12px}
.pc-feat li{padding:6px 0;border-bottom:1px solid var(--border-light);display:flex;align-items:center;gap:7px;color:var(--text2)}
.pc-feat li::before{content:'✓';color:var(--green);font-weight:700}.pc .btn{margin-top:16px;width:100%;justify-content:center}
.router-cmp{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:24px}
.router-good{background:var(--surface);border:2px solid var(--green);border-radius:var(--radius);padding:20px}
.router-bad{background:var(--surface);border:2px solid rgba(239,68,68,0.3);border-radius:var(--radius);padding:20px;opacity:0.7}
.rl{display:flex;justify-content:space-between;padding:8px 0;font-size:13px;border-bottom:1px solid var(--border-light)}.rl:last-child{border-bottom:none}
.dt{width:100%;border-collapse:collapse;font-size:13px;background:var(--surface);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow-sm)}
.dt th{background:#f9fafb;padding:10px 14px;text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--text2);font-weight:600;border-bottom:2px solid var(--border)}
.dt td{padding:10px 14px;border-bottom:1px solid var(--border-light)}.dt tr:hover td{background:#fafafa}
.code-block{background:#1e293b;color:#e2e8f0;border-radius:var(--radius);padding:22px;font-family:monospace;font-size:12px;line-height:1.8;overflow-x:auto;position:relative}
.code-block .c1{color:#86efac}.code-block .c2{color:#fbbf24}.code-block .c3{color:#60a5fa}.code-block .c4{color:#c4b5fd}.code-block .c5{color:#94a3b8}
.copy-btn{position:absolute;top:10px;right:10px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;padding:4px 10px;border-radius:4px;font-size:10px;cursor:pointer}
.privacy-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}
.privacy-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow-sm)}
.privacy-card h4{font-size:14px;margin-bottom:8px}
.privacy-card li{font-size:12px;color:var(--text2);padding:3px 0;list-style:none}
.privacy-card li::before{content:'·';margin-right:6px;color:var(--gold);font-weight:700}
.modal-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:200;align-items:center;justify-content:center;padding:20px}
.modal-overlay.open{display:flex}
.modal{background:var(--surface);border-radius:var(--radius);padding:30px 24px;max-width:440px;width:100%;box-shadow:var(--shadow-lg);max-height:90vh;overflow-y:auto;position:relative}
.modal h3{font-size:20px;margin-bottom:4px}.modal>p{color:var(--text2);font-size:13px;margin-bottom:20px}
.fg{margin-bottom:14px}.fg label{display:block;font-size:12px;font-weight:600;margin-bottom:4px}
.fg input,.fg select{width:100%;padding:10px 12px;border:1.5px solid var(--border);border-radius:8px;font-size:13px;font-family:inherit;background:var(--bg);transition:border 0.15s}
.fg input:focus,.fg select:focus{outline:none;border-color:var(--gold);box-shadow:0 0 0 3px var(--gold-light)}
.fg select{appearance:none;-webkit-appearance:none;background:var(--bg) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12'%3E%3Cpath d='M6 8L1 3h10z' fill='%236b7280'/%3E%3C/svg%3E") no-repeat right 10px center;padding-right:30px}
.fc{display:flex;align-items:flex-start;gap:8px;font-size:12px;color:var(--text2);margin-bottom:8px}.fc input{margin-top:2px;accent-color:var(--gold);width:15px;height:15px;flex-shrink:0}.fc a{color:var(--gold);font-weight:600}
.modal-close{position:absolute;top:12px;right:12px;background:none;border:none;font-size:22px;cursor:pointer;color:var(--text2)}
.chat-widget{position:fixed;bottom:20px;right:20px;z-index:150}
.chat-btn-w{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#b8860b,#9a6d0c);color:#fff;border:none;cursor:pointer;font-size:22px;box-shadow:0 4px 20px var(--gold-glow);display:flex;align-items:center;justify-content:center}
.chat-panel-w{display:none;position:absolute;bottom:64px;right:0;width:340px;max-height:480px;background:#fff;border-radius:var(--radius);box-shadow:var(--shadow-lg);overflow:hidden;border:1px solid var(--border)}
.chat-panel-w.open-w{display:flex;flex-direction:column}
.chat-header-w{background:linear-gradient(135deg,#b8860b,#9a6d0c);color:#fff;padding:12px 16px;font-weight:700;font-size:13px}
.chat-msgs-w{flex:1;overflow-y:auto;padding:12px;min-height:200px;max-height:300px;display:flex;flex-direction:column;gap:8px}
.msg-bot{background:#f3f4f6;padding:8px 12px;border-radius:10px 10px 10px 2px;font-size:12px;align-self:flex-start;max-width:85%}
.msg-user{background:var(--gold);color:#fff;padding:8px 12px;border-radius:10px 10px 2px 10px;font-size:12px;align-self:flex-end;max-width:85%}
.chat-input-w{display:flex;gap:6px;padding:10px;border-top:1px solid var(--border)}
.chat-input-w input{flex:1;padding:8px 12px;border:1px solid var(--border);border-radius:16px;font-size:12px;outline:none;font-family:inherit}
.chat-input-w button{width:32px;height:32px;border-radius:50%;background:var(--gold);color:#fff;border:none;cursor:pointer;font-size:14px;flex-shrink:0}
.chat-powered{text-align:center;font-size:9px;color:var(--text3);padding:6px;background:#f9fafb}
.lang-picker{position:relative}
.lang-trigger{display:flex;align-items:center;gap:4px;background:var(--surface);border:1.5px solid var(--border);padding:6px 10px;border-radius:20px;font-size:12px;cursor:pointer;color:var(--text);white-space:nowrap}
.lang-trigger:hover{border-color:var(--gold)}
.lang-drop{display:none;position:absolute;top:100%;right:0;margin-top:4px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);min-width:150px;max-height:280px;overflow-y:auto;z-index:50;box-shadow:var(--shadow-lg)}
.lang-picker.active .lang-drop{display:block}
.lang-drop a{display:flex;align-items:center;gap:6px;padding:8px 14px;color:var(--text2);text-decoration:none;font-size:11px;transition:all 0.1s}
.lang-drop a:hover,.lang-drop a.sel{background:var(--gold-light);color:var(--gold);font-weight:600}
.footer{border-top:1px solid var(--border);padding:40px 20px;text-align:center;font-size:12px;color:var(--text3)}
.footer-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;max-width:800px;margin:0 auto 20px;text-align:left}
.footer-grid h5{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:var(--text2);margin-bottom:12px}
.footer-grid a{display:block;color:var(--text3);text-decoration:none;font-size:12px;padding:2px 0}
.footer-grid a:hover{color:var(--gold)}
@media(max-width:768px){.nav-links{display:none}.hamburger{display:flex}.grid2,.grid3,.grid4,.router-cmp,.pricing-grid,.footer-grid{grid-template-columns:1fr}.pc.pop{transform:none}.chat-panel-w{width:calc(100vw-32px);right:-4px}.hero h1{font-size:26px}.sec{padding:50px 16px}.modal{max-width:100%}}@media(min-width:769px){.mobile-menu{display:none!important}}
</style>
</head>
<body>

<nav class="nav"><div class="nav-inner">
<a href="#" class="nav-logo"><b>◆</b>AICraft</a>
<div class="nav-links">
<a href="#models" data-i18n="nav_models">Models</a>
<a href="#pricing" data-i18n="nav_pricing">Pricing</a>
<a href="#router" data-i18n="nav_router">Auto Router</a>
<a href="#docs" data-i18n="nav_docs">Docs</a>
<a href="#privacy" data-i18n="nav_privacy">Privacy</a>
</div>
<div class="nav-r">
<div class="lang-picker" id="lp"><button class="lang-trigger" id="lt"><span id="lf">EN</span> ▾</button><div class="lang-drop" id="ld"></div></div>
<button class="nav-cta" onclick="openSignup()" data-i18n="nav_signup">Sign Up</button>
<button class="hamburger" id="hb" onclick="toggleMenu()"><span></span><span></span><span></span></button>
</div></div>
<div class="mobile-menu" id="mm">
<a href="#models" onclick="toggleMenu()" data-i18n="nav_models">Models</a>
<a href="#pricing" onclick="toggleMenu()" data-i18n="nav_pricing">Pricing</a>
<a href="#router" onclick="toggleMenu()" data-i18n="nav_router">Auto Router</a>
<a href="#docs" onclick="toggleMenu()" data-i18n="nav_docs">Docs</a>
<a href="#privacy" onclick="toggleMenu()" data-i18n="nav_privacy">Privacy</a>
<a href="#" onclick="toggleMenu();openSignup()" data-i18n="nav_signup" style="color:var(--gold);font-weight:600">Sign Up</a>
</div></nav>

<section class="hero">
<div class="hero-badge"><span class="dot"></span> <span data-i18n="hero_badge">7 Providers · 40+ Models · Live</span></div>
<h1><span data-i18n="hero_h1_p1">One API for</span> <em><span data-i18n="hero_h1_p2">every frontier model</span></em></h1>
<p data-i18n="hero_desc">Access DeepSeek, Qwen, GLM, MiniMax, Doubao, OpenRouter & more through a single endpoint. Our Auto Router picks the best model for every task — saving up to 93% vs GPT-4.</p>
<div class="hero-actions">
<a href="#pricing" class="btn btn-primary" data-i18n="hero_cta1">View Plans</a>
<a href="#docs" class="btn btn-outline" data-i18n="hero_cta2">API Docs</a>
<button class="btn btn-outline" onclick="openSignup()" data-i18n="hero_cta3">Create Free Account</button>
</div></section>

<section id="models" class="sec"><div class="sec-inner">
<div class="sec-label" data-i18n="models_label">Model Library</div>
<h2 class="sec-title" data-i18n="models_title">Every model, one endpoint</h2>
<p class="sec-sub" data-i18n="models_sub">40+ models across 7 providers. Text generation, video creation, image synthesis — all behind a single API key.</p>
<div class="tabs" id="mt"><button class="tab-btn active" data-tab="tc" data-i18n="tab_text_chinese">Text · Chinese</button><button class="tab-btn" data-tab="ti" data-i18n="tab_text_intl">Text · International</button><button class="tab-btn" data-tab="md" data-i18n="tab_media">Media Gen</button></div>
<div class="tab-panel active" id="tc"><div class="model-grid" id="gtc"></div></div>
<div class="tab-panel" id="ti"><div class="model-grid" id="gti"></div></div>
<div class="tab-panel" id="md"><div class="model-grid" id="gmd"></div></div>
</div></section>

<section id="pricing" class="sec" style="background:#fff;border-top:1px solid var(--border);border-bottom:1px solid var(--border)"><div class="sec-inner">
<div class="sec-label" data-i18n="pricing_label">Pricing</div>
<h2 class="sec-title" data-i18n="pricing_title">Simple, transparent, competitive</h2>
<p class="sec-sub" style="margin-bottom:30px" data-i18n="pricing_sub">All plans include OpenAI-compatible API + Auto Router. Pay only for what you use beyond included tokens.</p>
<div class="pricing-grid">
<div class="pc"><div class="pc-name" data-i18n="price_free">Free</div><div class="pc-amt">$0<small>/mo</small></div><div class="pc-tok" data-i18n="price_free_tokens">5M tokens · Chinese</div><ul class="pc-feat"><li data-i18n="price_free_f1">All Chinese text models</li><li data-i18n="price_free_f2">5 requests/min</li><li data-i18n="price_free_f3">Auto Router included</li><li data-i18n="price_free_f4">Community support</li></ul><button class="btn btn-outline" onclick="openSignup()" data-i18n="price_free_cta">Start Free</button></div>
<div class="pc pop"><div class="pc-name" data-i18n="price_starter">Starter</div><div class="pc-amt">$12<small>/mo</small></div><div class="pc-tok" data-i18n="price_starter_tokens">50M tokens · All Chinese</div><ul class="pc-feat"><li data-i18n="price_starter_f1">All Chinese text models</li><li data-i18n="price_starter_f2">Unlimited requests</li><li data-i18n="price_starter_f3">Auto Router · 3 tiers</li><li data-i18n="price_starter_f4">Email support</li><li data-i18n="price_starter_f5">Usage dashboard</li></ul><button class="btn btn-primary" onclick="openSignup()" data-i18n="price_starter_cta">Subscribe</button></div>
<div class="pc"><div class="pc-name" data-i18n="price_pro">Pro</div><div class="pc-amt">$39<small>/mo</small></div><div class="pc-tok" data-i18n="price_pro_tokens">200M tokens · Chinese</div><ul class="pc-feat"><li data-i18n="price_pro_f1">Everything in Starter</li><li data-i18n="price_pro_f2">Priority routing</li><li data-i18n="price_pro_f3">Advanced analytics</li><li data-i18n="price_pro_f4">Slack support</li></ul><button class="btn btn-outline" onclick="openSignup()" data-i18n="price_pro_cta">Go Pro</button></div>
<div class="pc glb"><div class="pc-name" data-i18n="price_global">Global</div><div class="pc-amt">$89<small>/mo</small></div><div class="pc-tok" data-i18n="price_global_tokens">300M · Chinese + Intl</div><ul class="pc-feat"><li data-i18n="price_global_f1">Everything in Pro</li><li data-i18n="price_global_f2">100M international models</li><li data-i18n="price_global_f3">GPT-4o · Claude · Gemini</li><li data-i18n="price_global_f4">Global routing</li></ul><button class="btn btn-outline" style="border-color:var(--blue);color:var(--blue)" onclick="openSignup()" data-i18n="price_global_cta">Go Global</button></div>
</div>
<div style="text-align:center;margin-top:14px;font-size:12px;color:var(--text2)"><span data-i18n="price_ent">Enterprise</span>: <span data-i18n="price_ent_desc">$299/mo · 2B tokens · Custom SLA</span> · <a href="#" style="color:var(--gold)" data-i18n="price_ent_cta">Contact Sales</a></div>
</div></section>

<section id="router" class="sec"><div class="sec-inner">
<div class="sec-label" data-i18n="router_label">Competitive Edge</div>
<h2 class="sec-title" data-i18n="router_title">The only platform with Auto Intelligent Routing</h2>
<p class="sec-sub" data-i18n="router_sub">OpenRouter doesn't have it. SiliconFlow doesn't have it. Qiniu doesn't have it. Only AICraft automatically selects the optimal model for every request.</p>
<div class="grid4" style="margin-top:24px">
<div class="card" style="text-align:center"><div style="font-size:28px">🧠</div><div style="font-weight:700;font-size:14px" data-i18n="router_stat1">6 Categories</div><div style="font-size:11px;color:var(--text2)" data-i18n="router_stat1_sub">Auto task detection</div></div>
<div class="card" style="text-align:center"><div style="font-size:28px">⚡</div><div style="font-weight:700;font-size:14px" data-i18n="router_stat2">0.3ms Overhead</div><div style="font-size:11px;color:var(--text2)" data-i18n="router_stat2_sub">$0.0000006 per call</div></div>
<div class="card" style="text-align:center"><div style="font-size:28px">🛡️</div><div style="font-weight:700;font-size:14px" data-i18n="router_stat3">Auto Fallback</div><div style="font-size:11px;color:var(--text2)" data-i18n="router_stat3_sub">Primary fails → backup</div></div>
<div class="card" style="text-align:center"><div style="font-size:28px">💰</div><div style="font-weight:700;font-size:14px" data-i18n="router_stat4">91% Avg Saving</div><div style="font-size:11px;color:var(--text2)" data-i18n="router_stat4_sub">vs GPT-4</div></div>
</div>
<div class="router-cmp">
<div class="router-good"><h4 style="color:var(--green);margin-bottom:10px" data-i18n="router_good_title">With AICraft Auto Router</h4><div class="rl"><span>💻 <span data-i18n="rt_coding">Coding</span></span><b>→ DeepSeek V3</b><span style="color:var(--green)">-93%</span></div><div class="rl"><span>🌐 <span data-i18n="rt_translation">Translation/Batch</span></span><b>→ V4-Flash</b><span style="color:var(--green)">-99%</span></div><div class="rl"><span>🇨🇳 <span data-i18n="rt_chinese">Chinese/Multilingual</span></span><b>→ Qwen-Max</b><span style="color:var(--green)">-88%</span></div><div class="rl"><span>✍️ <span data-i18n="rt_creative">Creative Writing</span></span><b>→ MiniMax M2.5</b><span style="color:var(--green)">-91%</span></div></div>
<div class="router-bad"><h4 style="color:var(--red);margin-bottom:10px" data-i18n="router_bad_title">Without (like OpenRouter)</h4><div class="rl"><span>💻 Coding</span><b>→ GPT-4o</b><span>$2.50/M</span></div><div class="rl"><span>🌐 Translation</span><b>→ GPT-4o</b><span>$2.50/M</span></div><div class="rl"><span>🇨🇳 Chinese</span><b>→ GPT-4o</b><span>$2.50/M</span></div><div class="rl"><span>✍️ Creative</span><b>→ GPT-4o</b><span>$2.50/M</span></div></div>
</div>
</div></section>

<section class="sec" style="padding-top:0"><div class="sec-inner">
<div style="overflow-x:auto"><table class="dt"><thead><tr><th data-i18n="rt_task">Task</th><th data-i18n="rt_primary">Primary Model</th><th data-i18n="rt_fallback">Fallback</th><th data-i18n="rt_budget">Budget Pick</th><th data-i18n="rt_save">vs GPT-4</th></tr></thead><tbody>
<tr><td data-i18n="rt_coding">Coding</td><td>DeepSeek V3</td><td>Qwen-Max</td><td>V4-Flash</td><td style="color:var(--green);font-weight:700">-93%</td></tr>
<tr><td data-i18n="rt_translation">Translation/Batch</td><td>V4-Flash</td><td>Qwen-Turbo</td><td>V4-Flash</td><td style="color:var(--green);font-weight:700">-99%</td></tr>
<tr><td data-i18n="rt_chinese">Chinese</td><td>Qwen-Max</td><td>GLM-5</td><td>Qwen-Turbo</td><td style="color:var(--green);font-weight:700">-88%</td></tr>
<tr><td data-i18n="rt_reasoning">Reasoning</td><td>GLM-5</td><td>DeepSeek V3</td><td>MiniMax M2.5</td><td style="color:var(--green);font-weight:700">-83%</td></tr>
<tr><td data-i18n="rt_creative">Creative</td><td>MiniMax M2.5</td><td>Qwen-Max</td><td>V4-Flash</td><td style="color:var(--green);font-weight:700">-91%</td></tr>
<tr><td data-i18n="rt_chat">Customer Service</td><td>Doubao Pro</td><td>Qwen-Turbo</td><td>V4-Flash</td><td style="color:var(--green);font-weight:700">-91%</td></tr>
</tbody></table></div>
</div></section>

<section id="docs" class="sec" style="background:#1e293b;color:#fff"><div class="sec-inner">
<div class="sec-label" style="color:#fbbf24" data-i18n="docs_label">Quick Start</div>
<h2 class="sec-title" style="color:#fff" data-i18n="docs_title">3 lines to integrate</h2>
<p class="sec-sub" style="color:#94a3b8" data-i18n="docs_sub">Drop-in replacement for OpenAI. Works with Python, Node, Go, Rust, curl — any HTTP client.</p>
<div class="code-block" style="margin-top:24px"><button class="copy-btn" onclick="navigator.clipboard.writeText('pip install openai\\nfrom openai import OpenAI\\nclient = OpenAI(api_key=chr(34)+chr(34),base_url=chr(34)+chr(34))\\nclient.chat.completions.create(model=chr(34)+chr(34),messages=[{role:chr(34)+chr(34),content:chr(34)+chr(34)}])')">Copy</button>
<span class="c1"># Install any OpenAI SDK</span>
pip install openai

<span class="c1"># Connect to AICraft</span>
<span class="c3">from</span> openai <span class="c3">import</span> OpenAI
client = OpenAI(
    <span class="c4">api_key</span>=<span class="c2">"sk-your-key"</span>,
    <span class="c4">base_url</span>=<span class="c2">"https://api.aicraftapi.com/v1"</span>
)

<span class="c1"># Use the Auto Router (recommended)</span>
r = client.chat.completions.create(
    <span class="c4">model</span>=<span class="c2">"auto"</span>,
    <span class="c4">messages</span>=[{<span class="c2">"role"</span>:<span class="c2">"user"</span>,<span class="c2">"content"</span>:<span class="c2">"Write a Python quicksort"</span>}]
)
<span class="c5"># → Auto-routed to DeepSeek V3</span>
<span class="c5"># → Saved 93% vs GPT-4</span></div></div></section>

<section id="privacy" class="sec"><div class="sec-inner">
<div class="sec-label" data-i18n="privacy_label">Trust & Compliance</div>
<h2 class="sec-title" data-i18n="privacy_title">Privacy by jurisdiction</h2>
<p class="sec-sub" data-i18n="privacy_sub">GDPR (EU) · PIPL (China) · LGPD (Brazil) · CCPA (California)</p>
<div class="privacy-grid" style="margin-top:24px">
<div class="privacy-card"><h4 data-i18n="privacy_data_title">Data Commitments</h4><li data-i18n="privacy_d1">No conversation content stored</li><li data-i18n="privacy_d2">TLS 1.3 encryption end-to-end</li><li data-i18n="privacy_d3">API keys cryptographically hashed</li><li data-i18n="privacy_d4">Chinese model data stays in China</li><li data-i18n="privacy_d5">International via Hetao data bubble</li><li data-i18n="privacy_d6">30-day max log retention</li></div>
<div class="privacy-card"><h4 data-i18n="privacy_gdpr_title">GDPR (EU/EEA)</h4><li data-i18n="privacy_gdpr_l1">AICraft as Data Processor</li><li data-i18n="privacy_gdpr_l2">SCCs for cross-border transfers</li><li data-i18n="privacy_gdpr_l3">Right to erasure (30 days)</li><li data-i18n="privacy_gdpr_l4">DPO: dpo@aicraftapi.com</li></div>
<div class="privacy-card"><h4 data-i18n="privacy_pipl_title">PIPL (China)</h4><li data-i18n="privacy_pipl_l1">受托处理者：AICraft</li><li data-i18n="privacy_pipl_l2">法律依据：合同必需+知情同意</li><li data-i18n="privacy_pipl_l3">数据跨境：河套数据气泡</li><li data-i18n="privacy_pipl_l4">联系：dpo@aicraftapi.com</li></div>
<div class="privacy-card"><h4 data-i18n="privacy_other_title">LGPD · CCPA</h4><li data-i18n="privacy_other_l1">LGPD: Operador de dados · SCCs</li><li data-i18n="privacy_other_l2">CCPA: We do NOT sell personal data</li><li data-i18n="privacy_other_l3">Right to know · Right to delete</li><li data-i18n="privacy_other_l4">privacy@aicraftapi.com</li></div>
</div>
<div style="text-align:center;margin-top:20px;padding:16px;background:var(--surface);border:2px solid var(--gold);border-radius:var(--radius)">
<input type="checkbox" id="consent" style="accent-color:var(--gold);width:16px;height:16px;margin-right:8px"><label for="consent" style="font-size:12px" data-i18n="consent_label">I agree to Privacy Policy & Terms of Service.</label>
</div></div></section>

<footer class="footer"><div class="sec-inner"><div class="footer-grid">
<div><h5 data-i18n="footer_product">Product</h5><a href="#models" data-i18n="footer_models">Models</a><a href="#pricing" data-i18n="footer_pricing">Pricing</a><a href="#router" data-i18n="footer_router">Auto Router</a><a href="#docs" data-i18n="footer_docs">Docs</a></div>
<div><h5 data-i18n="footer_company">Company</h5><a href="#" data-i18n="footer_about">About</a><a href="#" data-i18n="footer_blog">Blog</a><a href="#" data-i18n="footer_careers">Careers</a><a href="#" data-i18n="footer_contact">Contact</a></div>
<div><h5 data-i18n="footer_legal">Legal</h5><a href="#privacy" data-i18n="footer_privacy">Privacy Policy</a><a href="#" data-i18n="footer_terms">Terms of Service</a><a href="#" data-i18n="footer_dpa">DPA</a><a href="#" data-i18n="footer_sla">SLA</a></div>
<div><h5 data-i18n="footer_api">API</h5><a href="#docs" data-i18n="footer_docs">Reference</a><a href="#" data-i18n="footer_status">Status</a><a href="#" data-i18n="footer_github">GitHub</a><a href="#" data-i18n="footer_changelog">Changelog</a></div>
</div><p data-i18n="footer_copyright">© 2026 AICraft · Shenzhen AICreatrix Technology Co., Ltd. · Hetao SZ-HK STIC Zone · aicraftapi.com</p></div></footer>

<div class="modal-overlay" id="sm"><div class="modal">
<button class="modal-close" onclick="closeSignup()">×</button>
<h3 data-i18n="signup_title">Create your AICraft account</h3>
<p data-i18n="signup_sub">Free to start. No credit card required.</p>
<form onsubmit="submitSignup(event)">
<div class="fg"><label data-i18n="signup_email">Email</label><input type="email" required placeholder="you@example.com"></div>
<div class="fg"><label data-i18n="signup_password">Password</label><input type="password" required minlength="8"></div>
<div class="fg"><label data-i18n="signup_name">Full Name</label><input type="text" required></div>
<div class="fg"><label data-i18n="signup_country">Country / Region</label><select required><option value="" data-i18n="signup_country_select">Select...</option><option>Japan</option><option>Brazil</option><option>United States</option><option>China</option><option>South Korea</option><option>Thailand</option><option>Indonesia</option><option>Vietnam</option><option>India</option><option>United Kingdom</option><option>Germany</option><option>France</option><option>Singapore</option><option>Other</option></select></div>
<div class="fg"><label data-i18n="signup_usecase">How will you use AICraft?</label><select required><option value="" data-i18n="signup_usecase_select">Select...</option><option data-i18n="signup_usecase_1">Personal project</option><option data-i18n="signup_usecase_2">Startup / Small business</option><option data-i18n="signup_usecase_3">Enterprise / Company</option><option data-i18n="signup_usecase_4">Academic / Research</option><option data-i18n="signup_usecase_5">Just exploring</option></select></div>
<div class="fg"><label data-i18n="signup_source">How did you hear about us?</label><select><option value="" data-i18n="signup_source_select">Select (optional)</option><option data-i18n="signup_source_1">GitHub</option><option data-i18n="signup_source_2">Google Search</option><option data-i18n="signup_source_3">Dev.to / Hashnode</option><option data-i18n="signup_source_4">Reddit / Hacker News</option><option data-i18n="signup_source_5">Friend / Colleague</option><option data-i18n="signup_source_6">Social Media</option></select></div>
<div class="fc"><input type="checkbox" required><span data-i18n="signup_consent_privacy">I agree to the Privacy Policy and consent to data processing.</span></div>
<div class="fc"><input type="checkbox" required><span data-i18n="signup_consent_terms">I agree to the Terms of Service.</span></div>
<div class="fc"><input type="checkbox"><span data-i18n="signup_consent_crossborder">I understand international model requests may transit through OpenRouter (USA).</span></div>
<button type="submit" class="btn btn-primary" style="width:100%;justify-content:center;margin-top:10px" data-i18n="signup_submit">Create Account</button>
</form>
<p style="text-align:center;margin-top:12px;font-size:12px;color:var(--text2)"><span data-i18n="signup_login">Already have an account?</span> <a href="#" style="color:var(--gold)" data-i18n="signup_login_link">Sign in</a></p>
</div></div>

<div class="chat-widget">
<div class="chat-panel-w" id="cpw">
<div class="chat-header-w" data-i18n="chat_header">AICraft Assistant · AI-Powered</div>
<div class="chat-msgs-w" id="cmw"><div class="msg-bot" data-i18n="chat_greeting">Hi! Ask me anything about AICraft API, pricing, or getting started.</div></div>
<div class="chat-input-w"><input type="text" id="ciw" onkeydown="if(event.key==='Enter')sendChatW()"><button onclick="sendChatW()">→</button></div>
<div class="chat-powered" data-i18n="chat_powered">Powered by AICraft Auto Router</div>
</div>
<button class="chat-btn-w" id="cbw" onclick="toggleChatW()">💬</button>
</div>

<script>
// i18n data
var T=""" + json.dumps(T) + """;
var langs=[{code:"en",name:"English",flag:"EN"},{code:"zh",name:"中文",flag:"中文"},{code:"ja",name:"日本語",flag:"日本"},{code:"ko",name:"한국어",flag:"한국"},{code:"th",name:"ไทย",flag:"ไทย"},{code:"id",name:"Bahasa Indonesia",flag:"ID"},{code:"vi",name:"Tiếng Việt",flag:"VI"},{code:"es",name:"Español",flag:"ES"},{code:"pt",name:"Português",flag:"PT"}];
var ld=document.getElementById("ld");
langs.forEach(function(l){var a=document.createElement("a");a.href="#";a.textContent=l.flag+" "+l.name;a.onclick=function(e){e.preventDefault();setLang(l.code)};ld.appendChild(a)});
document.getElementById("lt").onclick=function(e){e.preventDefault();e.stopPropagation();document.getElementById("lp").classList.toggle("active")};
document.addEventListener("click",function(e){if(!document.getElementById("lp").contains(e.target))document.getElementById("lp").classList.remove("active")});
function setLang(c){var l=langs.find(function(x){return x.code===c})||langs[0];document.getElementById("lf").textContent=l.flag;localStorage.setItem("al",c);var d=T[c]||T.en;document.querySelectorAll("[data-i18n]").forEach(function(el){var k=el.getAttribute("data-i18n");if(d[k])el.textContent=d[k]});document.querySelectorAll(".lang-drop a").forEach(function(a){a.classList.remove("sel");if(a.textContent.includes(l.name))a.classList.add("sel")})}
setLang(localStorage.getItem("al")||"en");

// Models
var tcm=[{p:"DeepSeek",n:"DeepSeek V3",d:"Flagship model. #1 coding benchmark.",ctx:"128K",inp:"$0.14",out:"$0.28",c:"#2563eb"},{p:"DeepSeek",n:"DeepSeek V4-Flash",d:"Fastest & cheapest. Batch processing.",ctx:"128K",inp:"$0.003",out:"$0.01",c:"#2563eb"},{p:"DeepSeek",n:"DeepSeek R1",d:"Advanced reasoning with CoT.",ctx:"128K",inp:"$0.55",out:"$2.19",c:"#2563eb"},{p:"Alibaba",n:"Qwen-Max",d:"Best Chinese comprehension.",ctx:"32K",inp:"$0.35",out:"$1.40",c:"#f59e0b"},{p:"Alibaba",n:"Qwen-Plus",d:"Balanced performance & cost.",ctx:"32K",inp:"$0.10",out:"$0.40",c:"#f59e0b"},{p:"Alibaba",n:"Qwen-Turbo",d:"Fast & affordable.",ctx:"8K",inp:"$0.03",out:"$0.12",c:"#f59e0b"},{p:"Zhipu",n:"GLM-5",d:"Strong logical reasoning.",ctx:"128K",inp:"$0.70",out:"$2.80",c:"#7c3aed"},{p:"Zhipu",n:"GLM-5-Flash",d:"Fast variant.",ctx:"128K",inp:"$0.10",out:"$0.40",c:"#7c3aed"},{p:"MiniMax",n:"MiniMax M2.5",d:"Excellent creative writing.",ctx:"128K",inp:"$0.10",out:"$0.40",c:"#ec4899"},{p:"MiniMax",n:"MiniMax M3",d:"Latest generation.",ctx:"128K",inp:"$0.15",out:"$0.60",c:"#ec4899"},{p:"ByteDance",n:"Doubao Pro",d:"Natural conversation.",ctx:"32K",inp:"$0.06",out:"$0.24",c:"#10b981"},{p:"ByteDance",n:"Doubao Lite",d:"Lightweight & cheapest.",ctx:"8K",inp:"$0.008",out:"$0.03",c:"#10b981"}];
var tim=[{p:"OpenAI",n:"GPT-4o",d:"Multimodal flagship.",ctx:"128K",inp:"$2.50",out:"$10.00",c:"#22c55e"},{p:"OpenAI",n:"GPT-4o-mini",d:"Cost-effective.",ctx:"128K",inp:"$0.15",out:"$0.60",c:"#22c55e"},{p:"Anthropic",n:"Claude Sonnet 4",d:"Speed & capability.",ctx:"200K",inp:"$3.00",out:"$15.00",c:"#ef4444"},{p:"Google",n:"Gemma 3 27B",d:"Open-weight from Google.",ctx:"128K",inp:"$0.15",out:"$0.60",c:"#a855f7"},{p:"Mistral",n:"Mistral Large",d:"European frontier.",ctx:"128K",inp:"$2.00",out:"$8.00",c:"#06b6d4"},{p:"Meta",n:"Llama 4 Maverick",d:"Open frontier from Meta.",ctx:"1M",inp:"$0.20",out:"$0.80",c:"#f97316"},{p:"NVIDIA",n:"Nemotron Ultra",d:"550B MoE. Free tier.",ctx:"1M",inp:"FREE",out:"FREE",c:"#84cc16"}];
var mdm=[{p:"Kling",n:"Kling 2.0",d:"Text-to-video. Up to 2min.",ctx:"10s",inp:"$0.08",out:"-",c:"#f43f5e"},{p:"Alibaba",n:"Wan2.1",d:"VBench #1 video model.",ctx:"10s",inp:"$0.06",out:"-",c:"#f59e0b"},{p:"ByteDance",n:"Jimeng Video",d:"HD short videos.",ctx:"10s",inp:"$0.08",out:"-",c:"#10b981"},{p:"ByteDance",n:"Seedance",d:"Img+vid+audio input.",ctx:"11s",inp:"$0.10",out:"-",c:"#10b981"},{p:"ByteDance",n:"Jimeng Image",d:"Text-to-image HD.",ctx:"2K",inp:"$0.003",out:"-",c:"#3b82f6"},{p:"Stability",n:"SD3",d:"Open image gen.",ctx:"1K",inp:"$0.002",out:"-",c:"#8b5cf6"},{p:"OpenAI",n:"DALL-E 3",d:"Natural lang to image.",ctx:"1K",inp:"$0.04",out:"-",c:"#22c55e"}];
function rm(m,g){document.getElementById(g).innerHTML=m.map(function(m){return'<div class="mc"><div class="mc-top"><div class="mc-av" style="background:'+m.c+'">◆</div><div><div class="mc-n">'+m.n+'</div><div class="mc-p">'+m.p+'</div></div></div><div class="mc-d">'+m.d+'</div><div class="mc-tags"><span class="tag blu">📐 '+m.ctx+'</span><span class="tag grn">⬇ '+m.inp+'</span><span class="tag gld">⬆ '+m.out+'</span></div></div>'}).join("")}
rm(tcm,"gtc");rm(tim,"gti");rm(mdm,"gmd");
document.querySelectorAll(".tab-btn").forEach(function(b){b.onclick=function(){var t=this.dataset.tab;this.parentElement.querySelectorAll(".tab-btn").forEach(function(x){x.classList.remove("active")});this.classList.add("active");document.querySelectorAll(".tab-panel").forEach(function(p){p.classList.remove("active")});document.getElementById(t).classList.add("active")}});

// Mobile
function toggleMenu(){document.getElementById("hb").classList.toggle("open");document.getElementById("mm").classList.toggle("open")}

// Signup
function openSignup(){document.getElementById("sm").classList.add("open");document.body.style.overflow="hidden"}
function closeSignup(){document.getElementById("sm").classList.remove("open");document.body.style.overflow=""}
document.getElementById("sm").addEventListener("click",function(e){if(e.target===this)closeSignup()});
function submitSignup(e){e.preventDefault();alert("Thanks! Your account request has been submitted.");closeSignup()}

// Chat
function toggleChatW(){document.getElementById("cpw").classList.toggle("open-w")}
async function sendChatW(){var i=document.getElementById("ciw");var m=i.value.trim();if(!m)return;var ms=document.getElementById("cmw");ms.insertAdjacentHTML("beforeend",'<div class="msg-user">'+m.replace(/</g,"&lt;")+"</div>");i.value="";ms.insertAdjacentHTML("beforeend",'<div id="ty" class="msg-bot">...</div>');ms.scrollTop=ms.scrollHeight;try{var r=await fetch("/v1/chat/completions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({model:"auto",messages:[{role:"system",content:"You are AICraft AI assistant. Keep answers short."},{role:"user",content:m}],max_tokens:100})});var d=await r.json();document.getElementById("ty")?.remove();ms.insertAdjacentHTML("beforeend",'<div class="msg-bot">'+(d.choices?.[0]?.message?.content||"Please try again.").replace(/</g,"&lt;")+"</div>");ms.scrollTop=ms.scrollHeight}catch(e){document.getElementById("ty")?.remove()}
// Update chat greeting when language changes
var origSetLang = setLang;
setLang = function(c) { origSetLang(c); var d=T[c]||T.en; if(d.chat_greeting) { var fm = document.querySelector("#cmw .msg-bot"); if(fm) fm.textContent = d.chat_greeting; } if(d.chat_header) { var hd = document.querySelector(".chat-header-w"); if(hd) hd.textContent = d.chat_header; } if(d.chat_powered) { var pw = document.querySelector(".chat-powered"); if(pw) pw.textContent = d.chat_powered; } if(d.chat_placeholder) { document.getElementById("ciw").placeholder = d.chat_placeholder; } };
}
</script>
</body>
</html>"""

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Site generated: {len(html):,} bytes, {len(keys)} i18n keys × 9 languages = {len(keys)*9} translations")
