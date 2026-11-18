# 夢想方舟 CG ARK

社團法人臺灣產學策進會（TAIC）夢想方舟數位人才培育基地的 3D 互動介紹頁。

方舟從高雄港旅運中心出發：選一隻代表技能的動物上船，開船沿實際航道駛出高雄港，再沿途經過「實務訓練群島、新興科技海域、創業育成港灣、產業媒合大陸」四站。船上每間艙房可以點開看介紹，船員（產策成員）、業師和成對的動物都可以點，會說一句話。

## 怎麼看

- 線上版：開 GitHub Pages 網址（見本 repo 右側 About）
- 本機：在這個資料夾執行 `python3 -m http.server`，再開 <http://localhost:8000>（直接雙擊 index.html 會因為瀏覽器安全限制載不到模型）

## 怎麼改船員、業師和台詞

- 直接改 `roster.js`，裡面有每個欄位的說明
- 或在網址最後加上 `#edit`（或 `?edit`），例如 <https://vgwtw.github.io/cgark-ark/?edit>，在頁面上點船員、業師或大副換造型和台詞，改好按「複製全部設定」貼回 `roster.js`
- 也可以直接在 GitHub 網頁上編輯 `roster.js` 並 commit，網站約一分鐘後自動更新

目前名單上的姓名與台詞都是「待填」的暫定內容。

## 檔案

| 檔案 | 內容 |
|---|---|
| `index.html` | 頁面本體（three.js 由 CDN 載入） |
| `roster.js` | 船員、業師、大副與動物對應技能的設定 |
| `harbor-data.js` | 高雄港岸線（由 OpenStreetMap 海岸線轉成場景座標） |
| `harbor-buildings.js` | 港邊建築外框與高度（由 OpenStreetMap 建築資料轉換） |
| `models/` | Kenney 3D 模型（打包成 `kenney-models.json`）與貼圖 |

## 資料來源與授權

- 頁面文字整理自 [CG ARK 官方頁面](https://taic.cargo.site/cg-ark)；2023 年合作課程資訊來自[蕃薯藤新聞](https://n.yam.com/Article/20230428305095)
- 岸線與建築資料 © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors，依 [ODbL](https://opendatacommons.org/licenses/odbl/) 授權；`harbor-data.js` 與 `harbor-buildings.js` 為其衍生資料，同樣以 ODbL 提供
- 3D 模型：[Kenney](https://kenney.nl)（Pirate Kit、Furniture Kit、Mini Characters、Cube Pets），CC0，授權檔見 `models/LICENSE-*.txt`
- 3D 引擎：[three.js](https://threejs.org) r147（MIT）
- 地標造型參考建築師說明與 Wikimedia Commons 照片，為簡化示意，非實際比例模型

## 更新方式（給維護者）

原始檔在 `VGWSITE/cgark-ark/`，改完執行：

```bash
python3 cgark-ark/tools/export_site.py
```

再到 `cgark-ark-site/` commit 並 push。
