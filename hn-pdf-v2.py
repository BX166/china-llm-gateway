# Read the markdown and convert to HTML for PDF
import re

with open(r"c:\Users\Brian\Desktop\OPC\海南网信办会议准备.md", "r", encoding="utf-8") as f:
    md = f.read()

# Simple markdown-to-HTML conversion for the PDF
html = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<title>AICraft · 海南网信办会议准备</title>
<style>
@page { size: A4; margin: 16mm; }
body { font-family: 'PingFang SC','Microsoft YaHei',sans-serif; font-size: 9.5pt; line-height: 1.8; color: #1a1d23; max-width: 750px; margin: 0 auto; padding: 25px; }
.cover { text-align: center; padding: 35px 0; border-bottom: 3px solid #b8860b; margin-bottom: 30px; }
.cover h1 { font-size: 24px; margin: 8px 0; }
.cover h1 span { color: #b8860b; }
.cover p { color: #6b7280; font-size: 12px; }
h2 { font-size: 13pt; color: #b8860b; border-left: 4px solid #b8860b; padding-left: 10px; margin: 24px 0 8px; page-break-after: avoid; }
h3 { font-size: 10.5pt; margin: 12px 0 5px; }
p, li { color: #374151; }
strong { color: #1a1d23; }
table { width: 100%; border-collapse: collapse; margin: 6px 0; font-size: 8.5pt; page-break-inside: avoid; }
th { background: #1a1d23; color: #fff; padding: 5px 8px; text-align: left; font-size: 7.5pt; letter-spacing: 1px; }
td { padding: 5px 8px; border-bottom: 1px solid #e5e7eb; }
tr:nth-child(even) td { background: #f9fafb; }
pre, .code-block { background: #1e293b; color: #e2e8f0; padding: 12px 16px; border-radius: 6px; font-family: 'Cascadia Code',monospace; font-size: 8pt; line-height: 1.5; white-space: pre; overflow-x: auto; margin: 6px 0; }
.highlight { background: #fef9ef; border: 1px solid #d4a030; border-radius: 6px; padding: 10px 14px; margin: 6px 0; }
.highlight p { margin: 2px 0; }
blockquote { border-left: 3px solid #d4a030; padding-left: 12px; color: #6b7280; margin: 6px 0; font-style: italic; }
hr { border: none; border-top: 1px solid #e5e7eb; margin: 16px 0; }
ul, ol { margin: 3px 0; padding-left: 18px; }
li { padding: 1px 0; }
.footer { text-align: center; color: #9ca3af; font-size: 8pt; margin-top: 30px; padding-top: 10px; border-top: 1px solid #e5e7eb; }
@media print { body { padding: 0; } .page-break { page-break-before: always; } }
</style></head><body>
<div class="cover">
<h1>AICraft · 海南省网信办<span>会议准备</span></h1>
<p>2026年6月11日上午 · 深圳艾创矩阵科技有限公司 · 机密</p>
</div>
"""

# Convert markdown content to HTML
lines = md.split('\n')
i = 0
in_code = False
in_table = False

while i < len(lines):
    line = lines[i]

    # Skip the title (already in cover)
    if line.startswith('# ') and '海南' in line:
        i += 1
        continue
    if line.startswith('**时间：'):
        i += 1
        continue
    if line.startswith('**参会方：'):
        i += 1
        continue
    if line.startswith('---'):
        i += 1
        continue

    # Headers
    if line.startswith('## '):
        html += '<h2>' + line[3:] + '</h2>\n'
    elif line.startswith('### '):
        html += '<h3>' + line[4:] + '</h3>\n'
    # Code blocks
    elif line.startswith('```'):
        if not in_code:
            html += '<div class="code-block">'
            in_code = True
        else:
            html += '</div>\n'
            in_code = False
        i += 1
        continue
    elif in_code:
        html += line + '\n'
        i += 1
        continue
    # Tables
    elif '|' in line and line.count('|') >= 2:
        if not in_table:
            html += '<table>\n'
            in_table = True
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if all(c.startswith('-') or c.startswith(':') for c in cells):
            i += 1  # skip alignment row
            continue
        is_header = i + 1 < len(lines) and '|---' in lines[i + 1] if i + 1 < len(lines) else False
        tag = 'th' if is_header else 'td'
        html += '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>\n'
    else:
        if in_table:
            html += '</table>\n'
            in_table = False
        # Regular text
        if line.strip():
            if line.startswith('> '):
                html += '<blockquote><p>' + line[2:] + '</p></blockquote>\n'
            elif line.startswith('- ') or line.startswith('1. '):
                html += '<li>' + line[2:] + '</li>\n'
            elif line.startswith('**') and '：' in line:
                html += '<p><strong>' + line.replace('**', '') + '</strong></p>\n'
            else:
                # Bold text
                line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
                html += '<p>' + line + '</p>\n'
        else:
            html += '<br>\n'

    i += 1

if in_table:
    html += '</table>\n'
if in_code:
    html += '</div>\n'

html += '''
<div class="footer">
AICraft · 深圳艾创矩阵科技有限公司 · aicraftapi.com · 机密文件 · 2026年6月10日
</div></body></html>
'''

with open(r"c:\Users\Brian\xundao\hn-meeting-v2.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"Generated: {len(html)} bytes")
