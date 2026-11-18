#!/usr/bin/env python3
"""把 assets-src/models/ 底下的 Kenney .glb 模型打包成 docs/models/kenney-models.json。

Claude 網頁版不提供 .glb 檔，所以頁面改成讀這個 JSON（base64），再交給 GLTFLoader 解析。
貼圖（Textures/colormap.png）不打包，直接放在 docs/models/<分類>/Textures/。

新增模型：把 .glb 放進 assets-src/models/<分類>/，執行本程式，再在 index.html 用 '<分類>/<檔名>' 引用。
用法（在 repo 根目錄）：python3 tools/build_models_bundle.py
"""
import base64, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'assets-src' / 'models'
OUT = ROOT / 'docs' / 'models' / 'kenney-models.json'


def main():
    bundle = {}
    for f in sorted(SRC.rglob('*.glb')):
        key = f.relative_to(SRC).with_suffix('').as_posix()
        bundle[key] = base64.b64encode(f.read_bytes()).decode()
    OUT.write_text(json.dumps(bundle, separators=(',', ':')))
    print(f'{len(bundle)} models -> {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)')


if __name__ == '__main__':
    main()
