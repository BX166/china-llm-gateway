#!/usr/bin/env python3
"""Patch AICraft site: new pricing + router showcase"""

with open("/opt/aicraft/web/index.html", "r") as f:
    html = f.read()

# 1. Replace pricing section with new tiers
old_pricing = '''<div class="pricing-grid">
    <div class="price-card"><div class="price-name">Free</div><div class="price-amount">$0<sub>/mo</sub></div><div class="price-tokens">5M tokens included</div><ul class="price-features"><li>All Chinese models</li><li>5 req/min</li><li>Community support</li><li>Standard routing</li></ul><a href="#" class="btn btn-white" data-i18n="pricing_free_cta">Start Building</a></div>
    <div class="price-card hero"><div class="price-name">Starter</div><div class="price-amount">$9.9<sub>/mo</sub></div><div class="price-tokens">30M tokens included</div><ul class="price-features"><li>Chinese + Intl models</li><li>Unlimited requests</li><li>Auto intelligent routing</li><li>Email support</li><li>Usage dashboard</li></ul><a href="#" class="btn btn-primary" data-i18n="pricing_starter_cta">Subscribe Now</a></div>
    <div class="price-card"><div class="price-name">Pro</div><div class="price-amount">$49<sub>/mo</sub></div><div class="price-tokens">150M tokens included</div><ul class="price-features"><li>Everything in Starter</li><li>Priority routing</li><li>Advanced analytics</li><li>Slack support</li></ul><a href="#" class="btn btn-white" data-i18n="pricing_pro_cta">Go Pro</a></div>
    <div class="price-card"><div class="price-name">Enterprise</div><div class="price-amount">$199<sub>/mo</sub></div><div class="price-tokens">800M tokens included</div><ul class="price-features"><li>Everything in Pro</li><li>Dedicated cluster</li><li>99.5% SLA</li><li>24/7 support</li></ul><a href="#" class="btn btn-white" data-i18n="pricing_ent_cta">Contact Sales</a></div>
  </div>'''

new_pricing = '''<div class="pricing-grid">
    <div class="price-card"><div class="price-name">Free</div><div class="price-amount">$0<sub>/mo</sub></div><div class="price-tokens">5M tokens · Chinese models</div><ul class="price-features"><li>All Chinese models</li><li>5 req/min</li><li>Community support</li><li>Standard routing</li></ul><a href="#" class="btn btn-white">Start Free</a></div>
    <div class="price-card hero"><div class="price-name">Starter</div><div class="price-amount">$12<sub>/mo</sub></div><div class="price-tokens">50M tokens · All Chinese</div><ul class="price-features"><li>All Chinese models</li><li>Unlimited requests</li><li>Auto intelligent routing</li><li>Email support</li><li>Usage dashboard</li></ul><a href="#" class="btn btn-primary">Subscribe</a></div>
    <div class="price-card"><div class="price-name">Pro</div><div class="price-amount">$39<sub>/mo</sub></div><div class="price-tokens">200M tokens · Chinese</div><ul class="price-features"><li>Everything in Starter</li><li>Priority routing</li><li>Advanced analytics</li><li>Slack support</li></ul><a href="#" class="btn btn-white">Go Pro</a></div>
    <div class="price-card" style="border:2px solid #3b82f6;position:relative;"><div style="position:absolute;top:-11px;left:50%;transform:translateX(-50%);background:#3b82f6;color:#fff;font-size:9px;font-weight:700;padding:3px 14px;border-radius:12px;">GLOBAL</div><div class="price-name">Global</div><div class="price-amount">$89<sub>/mo</sub></div><div class="price-tokens">300M tokens · Chinese + Intl</div><ul class="price-features"><li>Everything in Pro</li><li>100M international models</li><li>GPT-4o, Claude, Gemini</li><li>Global routing</li></ul><a href="#" class="btn btn-white" style="border-color:#3b82f6;color:#3b82f6;">Go Global</a></div>
  </div>
  <div style="text-align:center;margin-top:12px;">
    <div class="price-card" style="display:inline-block;max-width:300px;text-align:center;">
      <div class="price-name">Enterprise</div>
      <div class="price-amount">$299<sub>/mo</sub></div>
      <div class="price-tokens">2B tokens · Custom SLA</div>
      <a href="#" class="btn btn-white" style="width:100%;">Contact Sales</a>
    </div>
  </div>'''

html = html.replace(old_pricing, new_pricing)

# 2. Add Router Showcase section right before the router section
old_router_start = '<section id="router" class="section"><div class="container">'
router_showcase = '''<section id="router-showcase" class="section" style="background:linear-gradient(135deg,#f8fafb 0%,#fff 50%,#fef9ef 100%);border-top:1px solid #e2e8f0;border-bottom:1px solid #e2e8f0;"><div class="container">
  <div class="sec-label">Why AICraft</div>
  <h2 class="sec-title">The only API platform with Auto Intelligent Routing</h2>
  <p class="sec-subtitle">No other aggregator — not OpenRouter, not SiliconFlow, not Qiniu — automatically selects the best model for each task. We do.</p>
  <div class="stats-grid" style="margin-top:30px;">
    <div class="stat-card"><div class="stat-icon">🧠</div><div class="stat-val g">6</div><div class="stat-label">Task Categories Auto-Detected</div></div>
    <div class="stat-card"><div class="stat-icon">⚡</div><div class="stat-val b">0.3ms</div><div class="stat-label">Classification Overhead</div></div>
    <div class="stat-card"><div class="stat-icon">🛡️</div><div class="stat-val w">Fallback</div><div class="stat-label">Auto-Switch if Model Fails</div></div>
    <div class="stat-card"><div class="stat-icon">📊</div><div class="stat-val p">3 Tiers</div><div class="stat-label">Save / Balanced / Quality</div></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:30px;">
    <div style="background:#fff;border:2px solid #e2e8f0;border-radius:14px;padding:20px;">
      <h4 style="color:#b8860b;margin-bottom:8px;">With AICraft Auto Router</h4>
      <div style="font-size:13px;line-height:2;color:#5a5f6b;">
        👨‍💻 Coding task → <b style="color:#3b82f6;">DeepSeek V3</b> (save 93%)<br>
        🌐 Translation → <b style="color:#3b82f6;">V4-Flash</b> (save 99%)<br>
        ✍️ Creative → <b style="color:#3b82f6;">MiniMax M2.5</b> (save 91%)<br>
        📊 Avg monthly saving: <b style="color:#10b981;">91% vs GPT-4</b>
      </div>
    </div>
    <div style="background:#fff;border:2px solid #ef4444;border-radius:14px;padding:20px;opacity:0.7;">
      <h4 style="color:#ef4444;margin-bottom:8px;">Without (like OpenRouter)</h4>
      <div style="font-size:13px;line-height:2;color:#5a5f6b;">
        👨‍💻 Coding task → <b>GPT-4o</b> ($2.50/M)<br>
        🌐 Translation → <b>GPT-4o</b> ($2.50/M)<br>
        ✍️ Creative → <b>GPT-4o</b> ($2.50/M)<br>
        📊 All tasks cost the same premium
      </div>
    </div>
  </div>
  <p style="text-align:center;margin-top:16px;font-size:12px;color:#94a3b8;">Classification cost: $0.0000006 per request — <b>10 million classifications cost only $6</b></p>
</div></section>

''' + old_router_start

html = html.replace(old_router_start, router_showcase)

with open("/opt/aicraft/web/index.html", "w") as f:
    f.write(html)

print("Patched v2 OK")
