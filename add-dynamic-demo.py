with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the entire demo section with a dynamic animated version
old_section = '<section class="demo-section">'
new_section = '''<section class="demo-section">
<div class="sec-label" style="color:#d4a030;text-align:center;margin-bottom:20px">HOW IT WORKS</div>
<h2 style="text-align:center;color:#f1f5f9;font-size:28px;font-weight:800;margin-bottom:40px">Your request. <span style="color:#d4a030">Auto-routed.</span> Best model. Done.</h2>

<div class="flow-container">
  <!-- Step 1 -->
  <div class="flow-step step-1">
    <div class="flow-icon">💻</div>
    <div class="flow-label">Your App</div>
    <div class="flow-code">model=<span style="color:#fbbf24">"auto"</span></div>
  </div>
  <div class="flow-arr">→</div>
  <!-- Step 2 -->
  <div class="flow-step step-2">
    <div class="flow-icon">🧠</div>
    <div class="flow-label">Auto Router</div>
    <div class="flow-code">Classifying task...</div>
  </div>
  <div class="flow-arr">→</div>
  <!-- Step 3 -->
  <div class="flow-step step-3">
    <div class="flow-icon">🎯</div>
    <div class="flow-label">Best Model</div>
    <div class="flow-code">DeepSeek V3</div>
  </div>
  <div class="flow-arr">→</div>
  <!-- Step 4 -->
  <div class="flow-step step-4">
    <div class="flow-icon">✅</div>
    <div class="flow-label">Response</div>
    <div class="flow-code" style="color:#10b981">Saved 93%</div>
  </div>
</div>

<div class="flow-examples">
  <div class="flow-example e1">
    <span>💻 Coding</span>
    <span class="flow-model">→ DeepSeek V3</span>
    <span class="flow-save">-93%</span>
  </div>
  <div class="flow-example e2">
    <span>🌐 Translation</span>
    <span class="flow-model">→ Flash</span>
    <span class="flow-save">-99%</span>
  </div>
  <div class="flow-example e3">
    <span>✍️ Creative</span>
    <span class="flow-model">→ MiniMax M2.5</span>
    <span class="flow-save">-91%</span>
  </div>
  <div class="flow-example e4">
    <span>🇨🇳 Chinese</span>
    <span class="flow-model">→ Qwen-Max</span>
    <span class="flow-save">-88%</span>
  </div>
</div>
</section>'''

# Add flow CSS
flow_css = '''
.flow-container { display: flex; align-items: center; justify-content: center; gap: 16px; max-width: 900px; margin: 0 auto 30px; }
.flow-step { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 20px 24px; text-align: center; min-width: 140px; transition: all 0.3s; position: relative; }
.flow-step:hover { background: rgba(255,255,255,0.1); border-color: rgba(212,160,48,0.4); transform: translateY(-2px); }
.flow-icon { font-size: 32px; margin-bottom: 6px; }
.flow-label { color: #f1f5f9; font-weight: 600; font-size: 14px; margin-bottom: 4px; }
.flow-code { color: #94a3b8; font-family: monospace; font-size: 11px; }
.flow-arr { font-size: 28px; color: #d4a030; animation: arrowPulse 1.5s infinite; }
.flow-arr:nth-child(2) { animation-delay: 0.3s; }
.flow-arr:nth-child(4) { animation-delay: 0.6s; }
.flow-arr:nth-child(6) { animation-delay: 0.9s; }
@keyframes arrowPulse { 0%,100% { opacity: 0.3; transform: translateX(0); } 50% { opacity: 1; transform: translateX(6px); } }
.flow-examples { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; max-width: 900px; margin: 0 auto; }
.flow-example { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 14px; font-size: 12px; display: flex; justify-content: space-between; align-items: center; color: #e2e8f0; animation: slideUp 0.5s ease both; }
.flow-example.e1 { animation-delay: 0.2s; } .flow-example.e2 { animation-delay: 0.4s; }
.flow-example.e3 { animation-delay: 0.6s; } .flow-example.e4 { animation-delay: 0.8s; }
@keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.flow-model { color: #60a5fa; font-weight: 500; }
.flow-save { color: #10b981; font-weight: 700; }
@media (max-width: 768px) { .flow-container { flex-direction: column; } .flow-arr { transform: rotate(90deg); } .flow-examples { grid-template-columns: 1fr 1fr; } }
'''

# Remove old demo terminal CSS
old_terminal_start = '.demo-visual { position: relative; }'
old_terminal_end = '.demo-stats { display: grid'
pos_start = html.find(old_terminal_start)
pos_end = html.find(old_terminal_end)
if pos_start > 0 and pos_end > pos_start:
    html = html[:pos_start] + html[pos_end:]

# Remove old demo grid and stats CSS
html = html.replace('.demo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; max-width: var(--max-w,1120px); margin: 0 auto; align-items: center; }', '')
html = html.replace('.demo-stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-top: 16px; }', '')
html = html.replace('.demo-stat { text-align: center; padding: 12px 8px; background: var(--surface,#fff); border-radius: 8px; border: 1px solid var(--border,#e5e7eb); }', '')
html = html.replace('body.dark .demo-stat { background: #1e293b; border-color: #334155; }', '')
html = html.replace('.demo-stat .val { font-size: 22px; font-weight: 800; color: var(--gold,#b8860b); }', '')
html = html.replace('.demo-stat .lbl { font-size: 10px; color: var(--text2,#6b7280); margin-top: 2px; }', '')

# Add flow CSS before the demo section CSS
html = html.replace('.demo-section { padding', flow_css + '\n.demo-section { padding')

# Replace old demo HTML
html = html.replace(old_section + html[html.find(old_section)+len(old_section):html.find('</section>', html.find(old_section))], new_section)

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dynamic flow demo added")
