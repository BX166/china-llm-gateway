
with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

currency_js = """
<script>
var rates={en:{code:"USD",sym:"$",rate:1},zh:{code:"CNY",sym:"U+FFE5",rate:7.25},ja:{code:"JPY",sym:"U+FFE5",rate:150},ko:{code:"KRW",sym:"U+20A9",rate:1350},th:{code:"THB",sym:"U+0E3F",rate:36},id:{code:"IDR",sym:"Rp",rate:16000},vi:{code:"VND",sym:"U+20AB",rate:25000},es:{code:"EUR",sym:"U+20AC",rate:0.92},pt:{code:"BRL",sym:"R$",rate:5.50}};
var usdPrices={free:0,starter:15,pro:45,global:89,enterprise:299};
function fmtPrice(usd,rate,sym){
  if(sym=="U+FFE5") sym="\\u00a5";
  else if(sym=="U+20A9") sym="\\u20a9";
  else if(sym=="U+0E3F") sym="\\u0e3f";
  else if(sym=="U+20AB") sym="\\u20ab";
  else if(sym=="U+20AC") sym="\\u20ac";
  var v=Math.round(usd*rate);
  if(v==0) return sym+"0";
  if(rate>=1000) return sym+v.toLocaleString();
  return sym+v;
}
function updatePrices(lang){
  var r=rates[lang]||rates.en;
  var els=document.querySelectorAll("[data-price]");
  els.forEach(function(el){
    var key=el.getAttribute("data-price");
    var usd=usdPrices[key];
    if(usd!==undefined){
      var orig=el.getAttribute("data-orig")||el.textContent;
      if(!el.getAttribute("data-orig"))el.setAttribute("data-orig",orig);
      el.textContent=fmtPrice(usd,r.rate,r.sym);
    }
  });
}
var origSetLang2=setLang;
setLang=function(c){origSetLang2(c);updatePrices(c);};
updatePrices(localStorage.getItem("al")||"en");
</script>
"""
html = html.replace("</body>", currency_js + "\n</body>")

# Tag price elements - find and tag them
# The main pricing amounts in .pc-amt divs
# We need to find each price card and tag the amount

# Free card: $0
html = html.replace(
    '<div class="pc-amt">$0<small>/mo</small></div>',
    '<div class="pc-amt" data-price="free">$0<small>/mo</small></div>'
)

# Update Starter price from $12 to $15 AND tag it
html = html.replace(
    '<div class="pc-amt">$12<small>/mo</small></div>',
    '<div class="pc-amt" data-price="starter">$15<small>/mo</small></div>'
)

# Update Pro price from $39 to $45 AND tag it
html = html.replace(
    '<div class="pc-amt">$39<small>/mo</small></div>',
    '<div class="pc-amt" data-price="pro">$45<small>/mo</small></div>'
)

# Tag Global price
html = html.replace(
    '<div class="pc-amt">$89<small>/mo</small></div>',
    '<div class="pc-amt" data-price="global">$89<small>/mo</small></div>'
)

# Tag Enterprise price in the text
html = html.replace(
    '$299/mo',
    '<span data-price="enterprise">$299</span>/mo'
)

# Also update the pricing sub to mention pay-per-use for international
old_sub = "All plans include OpenAI-compatible API + Auto Router. Pay only for what you use beyond included tokens."
new_sub = "All plans include OpenAI-compatible API + Auto Router. International models billed per-use. No hidden fees."
html = html.replace(old_sub, new_sub)

with open("/opt/aicraft/web/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Currency + pricing updated OK")
