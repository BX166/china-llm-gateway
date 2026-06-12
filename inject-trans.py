import re

with open("/opt/aicraft/web/index.html", "r") as f:
    html = f.read()

with open("/tmp/translate_output.txt", "r") as f:
    translations = f.read()

# Inject translations before setLang
html = html.replace("function setLang(code) {", translations + "\nfunction setLang(code) {")

with open("/opt/aicraft/web/index.html", "w") as f:
    f.write(html)

for lang in ["en", "zh", "ja", "ko", "th", "id", "vi", "es", "pt"]:
    count = len(re.findall(r'T\.' + lang + r'\["([^"]+)"\]', html))
    print(lang + ": " + str(count) + " keys")

print("Done")
