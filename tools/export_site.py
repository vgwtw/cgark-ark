#!/usr/bin/env python3
"""把根目錄的 index.html（Claude 網頁版原始頁）包成可獨立開啟的網頁，輸出到 docs/index.html。

Claude 網頁發布時會自動幫頁面包上 <!doctype html>、<head> 和基本樣式；
GitHub Pages 沒有這層，所以這裡補上。docs/ 裡其他檔案（roster.js、港口資料、模型）
是網站本身的檔案，這支程式不會動它們。

用法（在 repo 根目錄）：python3 tools/export_site.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'index.html'
OUT = ROOT / 'docs' / 'index.html'

HEAD = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="夢想方舟 CG ARK：從高雄港出發的 3D 方舟，選一隻代表技能的動物上船，沿途經過四座學習風景。">
<style>
  :root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  body { margin: 0; }
  img { max-width: 100%; }
  [hidden] { display: none !important; }
</style>
{title}</head>
<body>
"""
TAIL = "\n</body>\n</html>\n"


def main():
    page = SRC.read_text(encoding='utf-8')
    if page.startswith('<meta charset="utf-8">'):
        page = page[len('<meta charset="utf-8">'):].lstrip('\n')
    m = re.search(r'<title>.*?</title>\n?', page)
    title = m.group(0) if m else '<title>夢想方舟 CG ARK</title>\n'
    if m:
        page = page.replace(m.group(0), '', 1)
    page = page.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    OUT.write_text(HEAD.replace('{title}', title) + page + TAIL, encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
