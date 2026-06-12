"""Add animated product demo section to homepage"""

with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add demo CSS
demo_css = """
/* Product Demo Section */
.demo-section { padding: 60px 20px; background: #fff; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }
body.dark .demo-section { background: #0f172a; }
.demo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; max-width: var(--max-w,1120px); margin: 0 auto; align-items: center; }
.demo-visual { position: relative; }
.demo-terminal { background: #1e293b; border-radius: 12px; overflow: hidden; box-shadow: 0 12px 40px rgba(0,0,0,0.15); font-family: 'Cascadia Code',monospace; font-size: 12px; }
.demo-terminal .bar { background: #0f172a; padding: 10px 14px; display: flex; gap: 6px; }
.demo-terminal .bar span { width: 10px; height: 10px; border-radius: 50%; }
.demo-terminal .bar span:nth-child(1) { background: #ef4444; }
.demo-terminal .bar span:nth-child(2) { background: #f59e0b; }
.demo-terminal .bar span:nth-child(3) { background: #10b981; }
.demo-terminal .body { padding: 16px; line-height: 1.8; }
.demo-terminal .c1 { color: #86efac; } .demo-terminal .c2 { color: #fbbf24; } .demo-terminal .c3 { color: #60a5fa; } .demo-terminal .c4 { color: #c4b5fd; }
.demo-terminal .cursor { display: inline-block; width: 8px; height: 16px; background: #f1f5f9; animation: blink 1s infinite; vertical-align: text-bottom; }
@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0; } }
.demo-terminal .line { opacity: 0; animation: fadeIn 0.3s ease forwards; }
.demo-terminal .line:nth-child(1) { animation-delay: 0.2s; }
.demo-terminal .line:nth-child(2) { animation-delay: 0.6s; }
.demo-terminal .line:nth-child(3) { animation-delay: 1.0s; }
.demo-terminal .line:nth-child(4) { animation-delay: 1.4s; }
.demo-terminal .line:nth-child(5) { animation-delay: 1.8s; }
.demo-terminal .line:nth-child(6) { animation-delay: 2.2s; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.demo-stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-top: 16px; }
.demo-stat { text-align: center; padding: 12px 8px; background: var(--surface,#fff); border-radius: 8px; border: 1px solid var(--border,#e5e7eb); }
body.dark .demo-stat { background: #1e293b; border-color: #334155; }
.demo-stat .val { font-size: 22px; font-weight: 800; color: var(--gold,#b8860b); }
.demo-stat .lbl { font-size: 10px; color: var(--text2,#6b7280); margin-top: 2px; }
@media (max-width: 768px) { .demo-grid { grid-template-columns: 1fr; } }
"""

html = html.replace("</style>", demo_css + "\n</style>")

# Add demo section HTML after hero
demo_html = """
<section class="demo-section">
<div class="demo-grid">
<div class="demo-visual">
<div class="demo-terminal">
<div class="bar"><span></span><span></span><span></span></div>
<div class="body">
<div class="line"><span class="c1"># Install OpenAI SDK</span></div>
<div class="line">pip install openai</div>
<div class="line"></div>
<div class="line"><span class="c1"># Connect to AICraft</span></div>
<div class="line"><span class="c3">from</span> openai <span class="c3">import</span> OpenAI</div>
<div class="line">client = OpenAI(</div>
<div class="line">  api_key=<span class="c2">"sk-xxx"</span>,</div>
<div class="line">  base_url=<span class="c2">"https://api.aicraftapi.com/v1"</span>)</div>
<div class="line"></div>
<div class="line"><span class="c1"># Auto Router: AI picks the best model</span></div>
<div class="line">r = client.chat.completions.create(</div>
<div class="line">  model=<span class="c2">"auto"</span>,</div>
<div class="line">  messages=[{<span class="c4">"content"</span>:<span class="c2">"Write a Python quicksort"</span>}])</div>
<div class="line"></div>
<div class="line"><span class="c1"># Response headers:</span></div>
<div class="line"><span class="c1"># X-AICraft-Routed-To: deepseek-chat</span></div>
<div class="line"><span class="c1"># X-AICraft-Savings: 93% vs GPT-4  </span><span class="cursor"></span></div>
</div>
</div>
<div class="demo-stats">
<div class="demo-stat"><div class="val">7</div><div class="lbl">AI Providers</div></div>
<div class="demo-stat"><div class="val">40+</div><div class="lbl">Models</div></div>
<div class="demo-stat"><div class="val">93%</div><div class="lbl">Save vs GPT-4</div></div>
</div>
</div>
<div style="margin-top:-10px">
<h2 style="font-size:26px;font-weight:800;margin-bottom:8px;color:var(--text,#1a1d23)">3 lines of code.<br>40+ models at your fingertips.</h2>
<p style="color:var(--text2,#6b7280);font-size:15px;line-height:1.7;margin-bottom:16px">Drop-in replacement for OpenAI. Our Auto Router automatically selects the best model for every task — saving up to 93% compared to always using GPT-4. No more manual model switching. No more overpaying.</p>
<div style="display:flex;gap:6px;flex-wrap:wrap">
<span style="background:rgba(16,185,129,0.1);color:#10b981;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:600">Auto Router</span>
<span style="background:rgba(37,99,235,0.1);color:#2563eb;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:600">9 Languages</span>
<span style="background:rgba(184,134,11,0.1);color:#b8860b;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:600">HK PDPO Compliant</span>
<span style="background:rgba(139,92,246,0.1);color:#8b5cf6;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:600">Pay-as-you-go</span>
</div>
</div>
</div>
</section>
"""

# Insert after hero section end
html = html.replace('</div></section><!-- Models -->', '</div></section>' + demo_html + '\n<!-- Models -->')

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Product demo section added")
