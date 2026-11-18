# 夢想方舟 CG ARK

社團法人臺灣產學策進會（TAIC）夢想方舟數位人才培育基地的 3D 互動介紹頁。

方舟從高雄港旅運中心出發：選一隻代表技能的動物上船，開船沿實際航道駛出高雄港，再沿途經過「實務訓練群島、新興科技海域、創業育成港灣、產業媒合大陸」四站。船上每間艙房可以點開看介紹，船員（產策成員）、業師和成對的動物都可以點，會說一句話。

**線上版：<https://vgwtw.github.io/cgark-ark/>**

## 怎麼改船員、業師和台詞

- 直接在 GitHub 網頁上編輯 [`docs/roster.js`](docs/roster.js) 並 commit，網站約一分鐘後自動更新。檔案裡有每個欄位的說明。
- 或在網址最後加上 `?edit`（例如 <https://vgwtw.github.io/cgark-ark/?edit>），在頁面上點船員、業師或大副換造型和台詞，改好按「複製全部設定」，把內容貼進 `docs/roster.js`。

目前名單上的姓名與台詞都是「待填」的暫定內容。這個 repo 是公開的，填入的姓名和台詞也會公開。

## 資料夾

| 路徑 | 內容 |
|---|---|
| `index.html` | 頁面原始檔（Claude 網頁版用的格式，沒有 `<head>`） |
| `docs/` | GitHub Pages 發布的網站 |
| `docs/index.html` | 由 `tools/export_site.py` 從根目錄的 `index.html` 產生，**不要直接改** |
| `docs/roster.js` | 船員、業師、大副與動物對應技能的設定（可以直接改） |
| `docs/harbor-data.js` | 高雄港岸線（由 `tools/osm/` 產生） |
| `docs/harbor-buildings.js` | 港邊建築外框與高度（由 `tools/osm/` 產生） |
| `docs/models/` | 打包好的 Kenney 模型、貼圖、動物圖示與授權檔 |
| `assets-src/models/` | 原始 `.glb` 模型（由 `tools/build_models_bundle.py` 打包） |
| `tools/` | 輸出網頁、打包模型、轉換 OpenStreetMap 資料的程式 |

## 修改流程

在 repo 根目錄：

```bash
python3 tools/export_site.py
```

改了根目錄的 `index.html` 之後執行，更新 `docs/index.html`。

```bash
python3 tools/build_models_bundle.py
```

新增或替換 `assets-src/models/` 的模型之後執行。

港口岸線與建築的重新產生方式見 [`tools/osm/README.md`](tools/osm/README.md)。

本機預覽：

```bash
python3 -m http.server 8000 --directory docs
```

再開 <http://localhost:8000>。直接雙擊 html 檔會因為瀏覽器安全限制載不到模型。

## 資料來源與授權

- 頁面文字整理自 [CG ARK 官方頁面](https://taic.cargo.site/cg-ark)；2023 年合作課程資訊來自[蕃薯藤新聞](https://n.yam.com/Article/20230428305095)
- 岸線與建築資料 © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors，依 [ODbL](https://opendatacommons.org/licenses/odbl/) 授權；`docs/harbor-data.js`、`docs/harbor-buildings.js` 與 `tools/osm/` 裡的資料為其衍生資料，同樣以 ODbL 提供
- 3D 模型：[Kenney](https://kenney.nl)（Pirate Kit、Furniture Kit、Mini Characters、Cube Pets），CC0，授權檔見 `docs/models/LICENSE-*.txt`
- 3D 引擎：[three.js](https://threejs.org) r147（MIT），由 CDN 載入
- 地標造型參考建築師說明與 Wikimedia Commons、旅遊報導照片，為簡化示意，非實際比例模型
