# Harness Shop Kata

這是一個很小的電商網站，用來教 Martin Fowler 網站文章
[Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
裡的概念。  
重點不是電商功能，而是用一個看得到成果的小網站，示範 **guides、sensors、feedforward、feedback 與 human steering loop**。

## 講師請先看這份

不要直接從程式碼開始教。  
請先照 [TEACHING.md](TEACHING.md) 的循序流程帶課：

1. 先看網站。
2. 再問 agent 可能犯什麼錯。
3. 再看 `GUIDE.md`。
4. 再跑 `npm run harness`。
5. 再故意破壞 behaviour 與 architecture。
6. 最後才整理原文概念。

## 先看成果

```bash
npm install
npm start
```

打開：

```text
http://localhost:4173
```

你會看到 3 個商品、購物車、折扣碼與金額計算。

## 再看 Harness

```bash
npm run harness
```

這個指令會做兩件事：

1. 執行 `harness/check.js`，檢查 guide、架構邊界、HTML module script。
2. 執行 `npm test`，用 Node.js 內建 test runner 驗證購物車規格。

## 檔案很少

```text
.
├── GUIDE.md              # 修改前看的 guide，屬於 feedforward
├── README.md             # 教學手冊
├── index.html            # 小型電商頁面
├── server.mjs            # 本機靜態伺服器
├── harness/check.js      # 自訂 feedback sensor
├── src/
│   ├── app.js            # 畫面互動
│   └── cart.js           # 購物車商業邏輯
└── test/
    └── cart.test.js      # 行為測試
```

## 這堂課怎麼教

### 第 1 步：先讓學員看到網站

```bash
npm start
```

講師說：

> 這只是一個小電商網站。等一下我們不是要教怎麼做電商，而是要教怎麼把 coding agent 放進一個可控制的工程環境。

### 第 2 步：解釋 Guide 是 feedforward

打開：

```bash
open GUIDE.md
```

講師說：

> Guide 是動手前的控制。它先告訴工程師或 agent：商品規格是什麼、折扣怎麼算、運費怎麼算、哪個檔案可以做什麼。

### 第 3 步：解釋 Sensor 是 feedback

執行：

```bash
npm run harness
```

講師說：

> Sensor 是動手後的控制。它不是叫你相信 agent，而是讓 agent 或工程師做完後，立刻得到可修正的回饋。

### 第 4 步：故意破壞

把 `src/cart.js` 裡的免運門檻從 `1000` 改成 `900`，再跑：

```bash
npm run harness
```

你會看到測試失敗。這就是 feedback。

### 第 5 步：Steering loop

問學員：

> 如果同一種錯誤一直發生，我們應該只是不斷修 code，還是把錯誤轉成 guide 或 sensor？

正確答案是：更新 harness。

## 原文每個元件對應

| 原文元件 | 白話解釋 | 本專案怎麼示範 |
| --- | --- | --- |
| Harness | 圍繞 coding agent 的控制系統 | `GUIDE.md`、`harness/check.js`、`test/cart.test.js`、README |
| Guide | 修改前的指引 | `GUIDE.md` |
| Sensor | 修改後的檢查 | `npm run harness` |
| Feedforward | 錯誤發生前先引導 | 先讀 `GUIDE.md` 再改程式 |
| Feedback | 錯誤發生後給回饋 | 測試失敗或 `harness/check.js` 失敗 |
| Computational control | 可以由程式穩定執行的檢查 | Node test、`harness/check.js` |
| Inferential control | 需要人類或 LLM 做語意判斷 | README 的 review 問題與課堂討論 |
| Steering loop | 人類根據錯誤更新 harness | 錯誤重複發生時，修改 `GUIDE.md` 或新增 sensor |
| Keep quality left | 品質問題越早抓越好 | 修改後立刻跑 `npm run harness` |
| Maintainability harness | 維持程式容易讀、容易改 | sensor 禁止 `cart.js` 操作 DOM |
| Architecture fitness harness | 維持架構邊界 | `cart.js` 商業邏輯、`app.js` 畫面互動 |
| Behaviour harness | 驗證使用者看得見的行為 | `test/cart.test.js` 驗證折扣、運費、總價 |
| Harnessability | 程式是否容易被 harness 管理 | 購物車計算抽到純函式 `cart.js` |
| Harness template | 可複製的樣板 | 這個 repo 可以複製成其他小網站 kata |
| Human role | 人類負責目標、取捨、更新控制 | 講師決定哪些錯誤要變成 guide 或 sensor |
| Context engineering | 把 agent 需要的上下文放清楚 | `GUIDE.md`、README、測試名稱、檔案結構 |
| Ambient affordances | 環境本身讓人更容易做對 | 清楚的 `src/`、`test/`、`harness/` 目錄 |
| Ashby's Law / variety | 控制系統要能管住變化 | 專案刻意很小，讓 harness 足以控制 |
| Continuous drift / health sensors | 長期監控品質是否變差 | 可延伸成每日跑 `npm run harness` 或檢查文件和程式常數一致 |
| Open questions | harness 本身也要被維護 | 課後討論：sensor 夠不夠？guide 和測試會不會不一致？ |

## 三種 Regulation Categories

### 1. Maintainability Harness

目的：避免程式變難讀、難改。

本專案例子：

- `harness/check.js` 禁止 `src/cart.js` 出現 `document.` 或 `querySelector`。
- 這避免商業邏輯和畫面操作混在一起。

### 2. Architecture Fitness Harness

目的：保護架構特性。

本專案的架構特性：

```text
cart.js = 純購物車邏輯
app.js  = DOM 與事件
html    = 頁面結構
```

### 3. Behaviour Harness

目的：保護使用者真正看得見的行為。

本專案測試：

- 加商品後小計正確。
- `HARNESS10` 折扣正確。
- 滿 NT$1,000 免運。
- 未滿 NT$1,000 運費 NT$80。

## 課堂練習

### 練習 A：破壞 behaviour

把 `FREE_SHIPPING_THRESHOLD` 改錯，跑：

```bash
npm run harness
```

討論：

- 這是哪一種 feedback？
- 錯誤訊息夠不夠清楚？

### 練習 B：破壞 architecture

在 `src/cart.js` 加入：

```js
document.querySelector("#cart");
```

跑：

```bash
npm run harness
```

討論：

- 這是 maintainability harness 還是 architecture fitness harness？
- 如果 agent 看到這個錯誤，能不能修？

### 練習 C：做一次 steering loop

新增一條規則：

> 所有金額都要顯示 NT$。

請學員決定：

- 要寫進 `GUIDE.md` 嗎？
- 要新增 test 嗎？
- 要新增 sensor 嗎？

## 講師收尾

可以用這段話收尾：

> Harness Engineering 不是多裝幾個工具。它是把團隊知道的規格、架構、品質要求與常見錯誤，轉成 agent 在修改前看得到的 guides，以及修改後跑得動的 sensors。小網站也能示範這件事；真正上到大型專案，只是把這些 guides 與 sensors 逐步擴大。

## 查證來源

- Martin Fowler 網站原文：Harness Engineering 文章，說明 feedforward、feedback、guides、sensors、computational/inferential controls、steering loop、keep quality left、regulation categories、harnessability、templates 與 human role。
- Node.js 官方文件：Node.js 內建 test runner 可用 `node --test` 執行。
- MDN 文件：瀏覽器使用 ES modules 時，HTML script 需要 `type="module"`。

註：本次有嘗試使用 Context7 查 Node.js 文件，但目前該 MCP 回傳參數 schema 錯誤，因此改查 Node.js 與 MDN 官方文件。
