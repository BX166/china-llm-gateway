#!/usr/bin/env python3
"""Use AICraft API (DeepSeek) to translate all i18n keys into 7 languages"""

import json
import urllib.request
import re
import time

API = "http://localhost:3000/v1/chat/completions"
KEY = "sk-1e5b7ecd9ac1c8dc309ca2baa4fde9d9118c0a0788192182"

LANGUAGES = {
    "ja": "Japanese",
    "ko": "Korean",
    "th": "Thai",
    "id": "Indonesian",
    "vi": "Vietnamese",
    "es": "Spanish",
    "pt": "Brazilian Portuguese"
}

def translate_batch(keys_dict, target_lang, batch_size=40):
    """Translate a batch of English text to target language"""
    items = list(keys_dict.items())[:batch_size]

    prompt = f"Translate these website UI labels from English to {target_lang}. Keep them short and natural. Return ONLY a JSON object with the same keys and translated values. Keys that are product names (AICraft, DeepSeek, Qwen, GLM, MiniMax, Doubao, GPT-4o, Claude, Gemini, OpenRouter, Stripe, GitHub, Slack, DPA, SLA) should remain in English.\n\n"
    prompt += json.dumps(dict(items), ensure_ascii=False, indent=1)
    prompt += "\n\nReturn ONLY valid JSON:"

    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "temperature": 0.3
    }).encode()

    req = urllib.request.Request(API, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KEY}"
    })

    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
        content = resp["choices"][0]["message"]["content"]
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"  Error: {e}")

    return {}

# Get all English keys from the site
with open("/opt/aicraft/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract existing English translations
en_keys = {}
for m in re.finditer(r'T\.en\["([^"]+)"\]="([^"]*)"', html):
    key, val = m.groups()
    if key not in en_keys:
        en_keys[key] = val

print(f"English keys to translate: {len(en_keys)}")

# Also extract Chinese translations for reference
zh_keys = {}
for m in re.finditer(r'T\.zh\["([^"]+)"\]="([^"]*)"', html):
    key, val = m.groups()
    zh_keys[key] = val

# Find which keys need translation per language
current_translations = {}
for lang in LANGUAGES:
    current_translations[lang] = {}
    for m in re.finditer(rf'T\.{lang}\["([^"]+)"\]="([^"]*)"', html):
        key, val = m.groups()
        current_translations[lang][key] = val

# For each language, find missing keys and translate
for lang, lang_name in LANGUAGES.items():
    missing = {k: v for k, v in en_keys.items() if k not in current_translations[lang]}
    if not missing:
        print(f"\n{lang}: all {len(en_keys)} keys already translated ✅")
        continue

    print(f"\n{lang} ({lang_name}): translating {len(missing)} missing keys...")

    all_translated = {}
    keys_list = list(missing.keys())

    # Translate in batches
    for i in range(0, len(keys_list), 30):
        batch_keys = keys_list[i:i+30]
        batch = {k: en_keys[k] for k in batch_keys}

        result = translate_batch(batch, lang_name, len(batch))
        if result:
            all_translated.update(result)
            print(f"  Batch {i//30+1}: {len(result)} translated")
        else:
            print(f"  Batch {i//30+1}: failed")

        time.sleep(0.5)  # Rate limit

    if all_translated:
        # Generate JS insertion
        js_lines = []
        for key in sorted(all_translated.keys()):
            val = all_translated[key].replace('"', '\\"').replace('\n', ' ')
            js_lines.append(f'T.{lang}["{key}"]="{val}";')

        # Find where to insert - after the last T.{lang} line or before the /// comment
        with open("/tmp/translate_output.txt", "a") as f:
            f.write(f"\n// === {lang_name} ({lang}) - AI translated ===\n")
            f.write('\n'.join(js_lines) + '\n')

        print(f"  Total: {len(all_translated)} keys translated for {lang}")

    time.sleep(1)

print("\nTranslations saved to /tmp/translate_output.txt")
print("Done!")
