"""Add dark/light mode toggle to AICraft website"""

with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add dark mode CSS variables
dark_css = """
/* Dark mode */
body.dark { --bg: #0f172a; --surface: #1e293b; --border: #334155; --text: #f1f5f9; --text2: #94a3b8; --text3: #64748b; --gold: #d4a030; --gold-light: rgba(212,160,48,0.1); --shadow-sm: 0 1px 3px rgba(0,0,0,0.3); --shadow: 0 4px 16px rgba(0,0,0,0.3); }
body.dark .nav { background: rgba(15,23,42,0.95); border-bottom-color: #1e293b; }
body.dark .nav-links a:hover { background: #1e293b; }
body.dark .pc { background: #1e293b; border-color: #334155; }
body.dark .card { background: #1e293b; border-color: #334155; }
body.dark table th { background: #0f172a; }
body.dark .code-block { background: #000; }
body.dark .tab-btn { background: #1e293b; }
body.dark button.btn-outline { background: #1e293b; color: #94a3b8; }
body.dark .mc { background: #1e293b; border-color: #334155; }
body.dark .mc:hover { border-color: #d4a030; }
body.dark .chat-panel-w { background: #1e293b; border-color: #334155; }
body.dark .chat-msgs-w { background: #0f172a; }
body.dark .msg-bot { background: #1e293b; color: #e2e8f0; }
body.dark .chat-input-w { background: #1e293b; border-color: #334155; }
body.dark .chat-input-w input { background: #0f172a; border-color: #334155; color: #f1f5f9; }
body.dark .modal { background: #1e293b; }
body.dark .modal p { color: #94a3b8; }
body.dark .fg input, body.dark .fg select { background: #0f172a; border-color: #334155; color: #f1f5f9; }
body.dark .privacy-card { background: #1e293b; }
body.dark .privacy-card li { color: #94a3b8; }
body.dark .lang-trigger { background: #1e293b; border-color: #334155; color: #f1f5f9; }
body.dark .lang-drop { background: #1e293b; border-color: #334155; }
body.dark .lang-drop a { color: #94a3b8; }
body.dark .chat-powered { background: #0f172a; }
body.dark .par div { opacity: 0.05; }
body.dark .router-good { background: #1e293b; }
body.dark .router-bad { background: #1e293b; }
body.dark .dt { background: #1e293b; }
body.dark .dt th { background: #0f172a; }
body.dark .footer { background: #1e293b; }
body.dark tr:nth-child(even) td { background: rgba(255,255,255,0.02); }
/* Theme toggle button */
.theme-toggle { background: none; border: 1.5px solid var(--border); border-radius: 20px; cursor: pointer; font-size: 16px; padding: 6px 10px; line-height: 1; transition: all 0.2s; }
.theme-toggle:hover { border-color: var(--gold); }
"""

html = html.replace("</style>", dark_css + "\n</style>")

# 2. Add toggle button in nav
nav_add = '<button class="theme-toggle" id="theme-btn" onclick="toggleTheme()" title="深色/亮色切换">🌓</button>'
html = html.replace('<button class="nav-cta" onclick="openSignup()"', nav_add + '\n    <button class="nav-cta" onclick="openSignup()"')

# 3. Add toggle JS
theme_js = """
<script>
function toggleTheme() {
  var body = document.body;
  body.classList.toggle('dark');
  var isDark = body.classList.contains('dark');
  document.getElementById('theme-btn').textContent = isDark ? '☀️' : '🌙';
  localStorage.setItem('aicraft-theme', isDark ? 'dark' : 'light');
}
// Load saved theme
(function() {
  var saved = localStorage.getItem('aicraft-theme');
  if (saved === 'dark') {
    document.body.classList.add('dark');
    document.getElementById('theme-btn').textContent = '☀️';
  } else {
    document.getElementById('theme-btn').textContent = '🌙';
  }
})();
</script>
"""

html = html.replace("</body>", theme_js + "\n</body>")

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dark mode toggle added")
