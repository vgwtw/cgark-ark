# 高雄港岸線與建築資料

資料 © OpenStreetMap contributors，ODbL。轉成方舟場景座標：1 單位 = 10 公尺，原點在旅運中心碼頭外 46 公尺的水面，x 沿碼頭方向（東南東），z 朝港內水面。

## 檔案

| 檔案 | 內容 |
|---|---|
| `coast.json` | OSM 海岸線（`natural=coastline`），Overpass 下載 |
| `bldg.json` | OSM 建築與建築分段（`building`、`building:part`），Overpass 下載 |
| `geo.json` | 地標座標（Nominatim 查詢結果） |
| `terrain.py` | 由海岸線算出陸地格網與出港航線，寫出 `docs/harbor-data.js` |
| `bld.py` | 把建築外框轉成場景座標（`bld-scene.json`） |
| `bld_export.py` | 分類地標、補高度，寫出 `docs/harbor-buildings.js` |

## 重新產生

需要 Python 3 與 numpy。在本資料夾依序執行：

```bash
python3 terrain.py
```

```bash
python3 bld.py
```

```bash
python3 bld_export.py
```

## 重新下載 OSM 資料

Overpass 查詢（存成 `coast.json` / `bldg.json`）：

```text
[out:json][timeout:50];way["natural"="coastline"](22.598,120.262,22.628,120.306);out geom;
```

```text
[out:json][timeout:160];(way["building"](22.596,120.258,22.634,120.312);way["building:part"](22.596,120.258,22.634,120.312);relation["building"](22.596,120.258,22.634,120.312););out geom;
```

公用伺服器 `overpass-api.de` 忙碌時可改用 `overpass.kumi.systems`。
