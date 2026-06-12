#!/usr/bin/env python3
"""Patch AICraft site: add media models + ensure chat widget"""

with open("/opt/aicraft/web/index.html", "r") as f:
    html = f.read()

# 1. Add Media tab button
old_btn = '<button class="tab-btn" data-tab="all">All Models</button>'
new_btn = '<button class="tab-btn" data-tab="all">All Models</button>\n    <button class="tab-btn" data-tab="media">Media Gen</button>'
html = html.replace(old_btn, new_btn)

# 2. Add media tab content div
old_div = '<div class="tab-content" id="tab-all"><div class="model-grid" id="all-models"></div></div>'
new_div = old_div + '\n  <div class="tab-content" id="tab-media"><div class="model-grid" id="media-models"></div></div>'
html = html.replace(old_div, new_div)

# 3. Add media models data
media_js = """
var mediaModels=[{p:"Kling",n:"Kling 2.0",d:"AI video generation. Text-to-video, image-to-video. Up to 2min.",ctx:"10s vid",input:"from $0.08/vid",output:"-",cat:"media",color:"#f43f5e"},{p:"Kling",n:"Kling 2.0 Pro",d:"High-quality cinematic video generation.",ctx:"15s vid",input:"from $0.15/vid",output:"-",cat:"media",color:"#f43f5e"},{p:"Alibaba",n:"Wan2.1 (Wanxiang)",d:"VBench #1 video model. Text-to-video, image-to-video.",ctx:"10s vid",input:"from $0.06/vid",output:"-",cat:"media",color:"#f59e0b"},{p:"ByteDance",n:"Jimeng Video",d:"ByteDance video generation. High quality short videos.",ctx:"10s vid",input:"from $0.08/vid",output:"-",cat:"media",color:"#10b981"},{p:"ByteDance",n:"Seedance",d:"Image+video+audio multi-reference input. 11s output.",ctx:"11s vid",input:"from $0.10/vid",output:"-",cat:"media",color:"#10b981"},{p:"ByteDance",n:"Jimeng Image",d:"Text-to-image. High quality poster and character generation.",ctx:"2K",input:"from $0.003/img",output:"-",cat:"media",color:"#3b82f6"},{p:"Stability",n:"Stable Diffusion 3",d:"Open image generation with fine-grained control.",ctx:"1K",input:"from $0.002/img",output:"-",cat:"media",color:"#8b5cf6"},{p:"OpenAI",n:"DALL-E 3",d:"Latest DALL-E. Natural language image generation.",ctx:"1K",input:"from $0.04/img",output:"-",cat:"media",color:"#22c55e"}];
function renderMedia(){document.getElementById("media-models").innerHTML=mediaModels.map(function(m){return '<div class=\"model-card\"><div class=\"model-provider\"><div class=\"model-avatar\" style=\"background:'+m.color+'\">&#9670;</div><div><div class=\"model-name\">'+m.n+'</div><div class=\"model-company\">'+m.p+'</div></div></div><div class=\"model-desc\">'+m.d+'</div><div class=\"model-tags\"><span class=\"model-tag\">&#127916; '+m.ctx+'</span><span class=\"model-tag g\">'+m.input+'</span></div></div>'}).join("")}
"""
html = html.replace("renderModels('chinese');", media_js + "\nrenderModels('chinese');")

# 4. Patch tab click handler
old_handler = "if(this.parentElement.id==='model-tabs'){renderModels(t);this.parentElement.querySelectorAll('.tab-btn').forEach(x=>x.classList.remove('active'));this.classList.add('active')}"
new_handler = "if(this.parentElement.id==='model-tabs'){if(t==='media'){renderMedia()}else{renderModels(t)};this.parentElement.querySelectorAll('.tab-btn').forEach(x=>x.classList.remove('active'));this.classList.add('active')}"
html = html.replace(old_handler, new_handler)

with open("/opt/aicraft/web/index.html", "w") as f:
    f.write(html)

print("Patched OK")
