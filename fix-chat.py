with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

chat_js = """
async function sendChatW() {
  var i = document.getElementById('ciw');
  if (!i) return;
  var m = i.value.trim();
  if (!m) return;
  var ms = document.getElementById('cmw');
  if (!ms) return;
  ms.insertAdjacentHTML('beforeend', '<div class=\"msg-user\">' + m.replace(/</g, '&lt;') + '</div>');
  i.value = '';
  ms.insertAdjacentHTML('beforeend', '<div id=\"ty\" class=\"msg-bot\">...</div>');
  ms.scrollTop = ms.scrollHeight;
  try {
    var r = await fetch('/v1/chat/completions', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        model: 'auto',
        messages: [{role: 'system', content: 'You are AICraft AI assistant. Keep answers short.'}, {role: 'user', content: m}],
        max_tokens: 100
      })
    });
    var d = await r.json();
    var ty = document.getElementById('ty');
    if (ty) ty.remove();
    var reply = d.choices?.[0]?.message?.content || 'Sorry, please try again.';
    ms.insertAdjacentHTML('beforeend', '<div class=\"msg-bot\">' + reply.replace(/</g, '&lt;') + '</div>');
  } catch(e) {
    var ty = document.getElementById('ty');
    if (ty) ty.remove();
    ms.insertAdjacentHTML('beforeend', '<div class=\"msg-bot\">Connection error. Try again later.</div>');
  }
  ms.scrollTop = ms.scrollHeight;
}
"""

# Insert sendChatW before the model data
marker = 'var tcm=[{p:"DeepSeek"'
html = html.replace(marker, chat_js + '\n' + marker)

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("sendChatW restored")
