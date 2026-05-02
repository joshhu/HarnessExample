# Harness Engineering 循序教學流程

這份文件才是本專案的主教材。  
請講師先讀這份，再看 `README.md`、`GUIDE.md`、程式碼與測試。

本課程的重點不是電商網站。  
電商網站只是容易看懂的載體，用來示範：

> 如何把 coding agent 放進一個由 guides、sensors、feedback、human steering 組成的工程控制系統。

## 0. 講師心法：不要一開始講完所有名詞

如果一開始就把 Harness、Feedforward、Feedback、Computational、Inferential、Steering loop 全部丟給學員，學員會覺得抽象。

這堂課應該照這個順序：

1. 先看一個很小的網站。
2. 再問「如果叫 agent 改它，會怕什麼？」
3. 再讓學員看到「修改前的 guide」。
4. 再讓學員看到「修改後的 sensor」。
5. 再故意破壞，讓 sensor 失敗。
6. 再引出文章名詞。
7. 最後才整理完整 Harness Engineering 地圖。

換句話說：

> 先讓學員感受到問題，再給名詞。

## 1. 課程目標

上完課後，學員應該能回答：

- Harness Engineering 解決什麼問題？
- Guide 和 Sensor 差在哪裡？
- Feedforward 和 Feedback 差在哪裡？
- Computational control 和 Inferential control 差在哪裡？
- 為什麼同一種錯誤重複出現時，要改 harness，而不是只改 code？
- 為什麼品質檢查要往左移？
- Maintainability harness、Architecture fitness harness、Behaviour harness 各管什麼？
- 小專案如何轉成自己團隊的 harness template？
- 人類在 agent 時代負責什麼？

## 2. 課前準備

講師先執行：

```bash
npm install
npm run harness
```

預期結果：

```text
[harness-pass] guide, article checklist, and architecture boundaries passed
tests 7
pass 7
```

再啟動網站：

```bash
npm start
```

打開：

```text
http://localhost:4173
```

## 3. 90 分鐘課程流程

| 時間 | 階段 | 目的 |
| --- | --- | --- |
| 0-10 分 | 看網站，不講 harness | 建立共同情境 |
| 10-20 分 | 問 agent 可能犯什麼錯 | 讓學員感受到風險 |
| 20-35 分 | 介紹 `GUIDE.md` | 引出 guide / feedforward |
| 35-50 分 | 跑 `npm run harness` | 引出 sensor / feedback |
| 50-65 分 | 故意破壞 behaviour | 讓 feedback 具體化 |
| 65-75 分 | 故意破壞 architecture | 引出 architecture fitness |
| 75-85 分 | 做 steering loop | 引出 human role |
| 85-90 分 | 原文概念總整理 | 把名詞對回文章 |

## 4. 逐步教學腳本

### Step 1：先看網站，不講 Harness

講師操作：

```bash
npm start
```

打開 `http://localhost:4173`。

示範：

1. 點「通勤背包」。
2. 點「保溫杯」。
3. 讓學員看見：
   - 小計 NT$1,200
   - 折扣 NT$120
   - 運費 NT$0
   - 總金額 NT$1,080

講師說：

> 這只是一個很小的電商網站。它有商品、購物車、折扣碼、免運門檻。今天重點不是網站，而是如果我們請 coding agent 修改這個網站，要如何降低它改錯的機率。

這一步不要講文章名詞。

學員此時只需要知道：

- 這是一個小網站。
- 有看得到的行為。
- 等一下會用它示範 agent 開發風險。

### Step 2：問學員「如果叫 agent 改它，會怕什麼？」

講師問：

> 如果我請 coding agent 幫這個網站加功能或修 bug，你會擔心它犯什麼錯？

請學員回答，講師寫在白板。

常見答案：

- 折扣算錯。
- 免運門檻改錯。
- 總金額算錯。
- UI 能看但商業邏輯壞掉。
- 把 DOM 操作寫進商業邏輯。
- 忘記補測試。
- README 寫一套，程式做另一套。

講師說：

> 這些擔心，就是 Harness Engineering 要處理的東西。它不是讓 agent 變完美，而是把常見錯誤變成前置指引和後置檢查。

此時才第一次講：

- 修改前的指引叫 guide。
- 修改後的檢查叫 sensor。

### Step 3：打開 `GUIDE.md`，引出 Guide / Feedforward

講師操作：

```bash
open GUIDE.md
```

講師帶讀三段：

1. 產品規格。
2. 架構規則。
3. 故意破壞示範。

講師說：

> `GUIDE.md` 是修改前看的文件。它在 agent 或工程師動手前，先告訴他哪些事情要做對、哪些邊界不能跨。這就是文章說的 guide，也就是 feedforward control。

板書：

```text
Guide = 修改前的指引
Feedforward = 錯誤發生前先降低機率
```

對應文章：

- Guides anticipate the agent's behaviour。
- Guides aim to steer before the agent acts。

對應本專案：

```text
GUIDE.md
```

講師提問：

> 如果沒有 `GUIDE.md`，agent 可能不知道哪些規格？

預期回答：

- `HARNESS10` 是 10% 折扣。
- 滿 NT$1,000 免運。
- `cart.js` 不可以碰 DOM。

### Step 4：跑 `npm run harness`，引出 Sensor / Feedback

講師操作：

```bash
npm run harness
```

講師說：

> Guide 是動手前的控制，但光有 guide 不夠。agent 可能還是會改錯。所以我們需要修改後的 sensor 來觀察結果，並給 feedback。

板書：

```text
Sensor = 修改後的檢查
Feedback = 錯誤發生後，把偏差回饋回來
```

對應本專案：

```text
harness/check.js
test/cart.test.js
npm run harness
```

說明 `npm run harness` 做兩件事：

1. `harness/check.js` 檢查文件與架構邊界。
2. `node --test` 執行購物車行為測試。

講師提醒：

> sensor-pass 不代表網站絕對正確，只代表目前這組 sensors 沒有偵測到問題。

這句話對應文章 sidebar：Metaphors only go so far。

### Step 5：故意破壞 Behaviour Harness

講師操作：

打開：

```bash
open src/cart.js
```

把：

```js
export const FREE_SHIPPING_THRESHOLD = 1000;
```

改成：

```js
export const FREE_SHIPPING_THRESHOLD = 900;
```

執行：

```bash
npm run harness
```

預期：

- behaviour test 失敗。

講師說：

> 這是 behaviour harness。它保護使用者看得見的行為：滿 NT$1,000 免運，而不是滿 NT$900。

板書：

```text
Behaviour harness = 保護功能行為
```

對應文章：

- Behaviour harness 用功能規格當 feedforward。
- 用測試與人工驗證當 feedback。
- 但不能盲目信任 AI 自己產生的測試。

講師延伸：

> 真實專案中，這裡可以再加入 approved fixtures。也就是由人類確認過的範例資料，不是 agent 自己隨便生的測試。

修回：

```js
export const FREE_SHIPPING_THRESHOLD = 1000;
```

### Step 6：故意破壞 Architecture Fitness Harness

講師操作：

在 `src/cart.js` 最下面加：

```js
document.querySelector("#cart-items");
```

執行：

```bash
npm run harness
```

預期：

```text
[harness-fail] src/cart.js must stay pure and must not touch DOM APIs
```

講師說：

> 這次不是金額算錯，而是架構邊界壞掉。`cart.js` 應該是純商業邏輯，DOM 操作應該留在 `app.js`。

板書：

```text
Architecture fitness harness = 保護架構特性
```

對應文章：

- Architecture fitness harness 用 guides 描述架構特性。
- 用 structural tests 或自訂 sensors 檢查邊界。

修掉剛剛新增的 DOM 程式碼。

### Step 7：引出 Maintainability Harness

講師說：

> 剛剛那個 DOM 檢查同時也是 maintainability harness。因為商業邏輯和 UI 混在一起，未來會更難測、更難改。

板書：

```text
Maintainability harness = 保護可維護性
```

對應本專案：

```text
harness/check.js
```

它檢查：

- `src/cart.js` 不可出現 `document.`
- 不可出現 `querySelector`
- 不可出現 `innerHTML`
- 不可出現 `addEventListener`

講師補充：

> 在真實專案中，maintainability harness 可能是 ESLint、type checker、coverage、duplicate code detector、complexity scanner。

### Step 8：Computational vs Inferential

現在學員已看過 guide 與 sensor，可以引出文章第二個大分類。

講師板書：

```text
Computational = deterministic、快、便宜、可重複
Inferential   = 語意判斷、較慢、較貴、較不穩定
```

本專案 computational controls：

```text
node --test
harness/check.js
```

本專案 inferential controls：

```text
講師 review
學員討論
README 中的反思問題
```

講師問：

> 判斷「總金額算對」適合 computational 還是 inferential？

答案：

- computational，因為可用測試明確驗證。

講師再問：

> 判斷「這個抽象會不會過度設計」適合 computational 還是 inferential？

答案：

- inferential，因為需要語意與經驗判斷。

### Step 9：Keep Quality Left

講師說：

> 品質問題越早發現越便宜。Harness Engineering 要把 feedback sensor 放在越左邊越好。

板書：

```text
修改前：看 GUIDE.md
修改後：立刻 npm run harness
PR 前：人工或 AI review
CI：重跑 sensors
長期：drift / health sensors
```

本專案最左邊的做法：

```bash
npm run harness
```

講師說：

> 這個指令應該在 commit 前就跑，而不是等到最後 review 才發現。

### Step 10：Steering Loop

講師問：

> 如果 agent 第二次又把 DOM 操作寫進 `cart.js`，我們該怎麼辦？

不要只回答「叫它改回來」。

正確方向：

1. 改 `GUIDE.md`，把規則寫得更清楚。
2. 改 `harness/check.js`，讓錯誤訊息更明確。
3. 如果需要，新增 test。

板書：

```text
同一種錯誤第一次出現：修 code
同一種錯誤第二次出現：修 harness
```

對應文章：

- The human's job is to steer the agent by iterating on the harness。

課堂活動：

請學員選一個 failure mode：

- 忘記 NT$ 格式。
- 折扣碼大小寫處理錯。
- README 漏掉某個文章觀念。
- `cart.js` 偷偷操作 DOM。

請學員決定：

- 要新增 guide？
- 要新增 sensor？
- 要新增 test？
- 還是需要人工 review？

### Step 11：Harnessability

講師說：

> 有些程式天生比較容易被 harness 管，有些很難。這叫 harnessability。

本專案提高 harnessability 的方式：

- `src/cart.js` 是純函式邏輯。
- `src/app.js` 才操作 DOM。
- 測試可以不開瀏覽器就驗證金額邏輯。
- `harness/check.js` 可以用文字掃描檢查架構邊界。

反例：

```text
如果所有計算都寫在 index.html onclick 裡，測試和 sensor 都會難很多。
```

講師說：

> Agent 時代的程式設計，不只是寫給人看，也要寫給測試、sensor、agent 理解。

### Step 12：Harness Template

講師說：

> 這個小專案不是要當正式電商網站，而是 harness template。

可複製的結構：

```text
GUIDE.md
README.md
src/
test/
harness/
npm run harness
```

換成其他網站也一樣：

| 網站 | Behaviour harness 可以測什麼 |
| --- | --- |
| 訂房網站 | 日期、房價、稅金、取消規則 |
| 報名網站 | 名額、費用、email 格式 |
| 會員網站 | 登入狀態、權限、表單驗證 |
| 電商網站 | 折扣、運費、庫存、總價 |

### Step 13：Human Role

講師說：

> Harness Engineering 不是把人拿掉，而是讓人不用一直抓重複錯誤。

人類負責：

- 決定什麼規格重要。
- 決定哪些錯誤值得做成 sensor。
- 決定哪些判斷只能人工 review。
- 當 sensor 太吵或太弱時調整 harness。
- 管理 guides 和 sensors 是否仍然符合產品方向。

對應文章：

- Human steers both guides and sensors。

### Step 14：Context Engineering 與 Ambient Affordances

講師說：

> Context engineering 是讓 agent 看得到需要的上下文。Harness engineering 是把這些上下文和檢查組成控制系統。

本專案 context：

```text
GUIDE.md
README.md
test/cart.test.js
harness/check.js
清楚的檔案命名
```

Ambient affordances 是環境自然給出的提示。

本專案例子：

- `src/cart.js` 讓人一看就知道是邏輯。
- `src/app.js` 讓人一看就知道是 UI。
- `test/` 讓人知道測試在哪。
- `harness/` 讓人知道自訂檢查在哪。

講師問：

> 如果這些檔案全部叫 `main.js`、`helper.js`、`stuff.js`，agent 會不會更容易做錯？

答案通常是會。

### Step 15：Ashby's Law / Variety

講師說：

> 被控制的系統越複雜，控制系統也要越有能力。這就是文章提到 Ashby's Law 的用意。

本專案刻意很小：

- 3 個商品。
- 1 個折扣碼。
- 1 個免運規則。
- 1 個商業邏輯檔。
- 1 個 harness 檢查器。

原因：

> 初學時先降低 variety，讓學員看懂 harness 怎麼運作。

講師補充：

> 真實大型專案不能只靠這麼小的 harness。你要逐步增加 guides、tests、static analysis、CI、runtime monitoring。

### Step 16：Continuous Drift / Health Sensors

講師說：

> 有些問題不是某一次 commit 造成，而是慢慢累積。

例子：

- README 寫的規格和程式常數不一致。
- 測試越來越弱。
- 沒人更新 guide。
- sensor 永遠不失敗，代表可能太弱。
- dependencies 老化。

本專案可以延伸：

- 每天跑 `npm run harness`。
- 新增 sensor 檢查 README 的免運門檻是否和 `cart.js` 一致。
- 新增 coverage 或 mutation testing。

### Step 17：Open Questions

課程最後不要假裝所有問題都解決了。文章也提醒，Harness Engineering 還有很多開放問題。

請用這些問題收尾：

1. 如果 guide 和 test 寫的不一致，agent 該相信誰？
2. 如果 sensor 從來不失敗，是品質很好，還是 sensor 太弱？
3. 哪些錯誤值得做成 computational sensor？
4. 哪些錯誤只能靠 inferential review？
5. 團隊誰負責維護 harness？
6. Harness 本身需不需要 code review？

講師總結：

> Harness 也是產品的一部分。它會老化，也需要維護。

## 5. 原文概念出現順序

不要照文章目錄硬講。建議照這個順序引出：

| 教學順序 | 原文概念 | 為什麼這時候講 |
| --- | --- | --- |
| 1 | Harness | 學員先看到 agent 風險後，再說需要外層控制系統 |
| 2 | Guide / Feedforward | 打開 `GUIDE.md` 時講 |
| 3 | Sensor / Feedback | 跑 `npm run harness` 時講 |
| 4 | Behaviour harness | 破壞免運門檻時講 |
| 5 | Architecture fitness harness | 破壞 `cart.js` DOM 邊界時講 |
| 6 | Maintainability harness | 說明為什麼邏輯和 UI 分離時講 |
| 7 | Computational vs Inferential | 學員看過測試和人工討論後講 |
| 8 | Keep quality left | 學員知道 sensor 後講時間點 |
| 9 | Steering loop | 問錯誤重複發生怎麼辦時講 |
| 10 | Harnessability | 解釋為何 `cart.js` 要是純函式時講 |
| 11 | Harness templates | 學員理解小專案後講如何複製 |
| 12 | Human role | 收斂到人類工作改變 |
| 13 | Context engineering | 補充 agent 需要看得到上下文 |
| 14 | Ambient affordances | 補充檔案命名和目錄結構也是提示 |
| 15 | Ashby's Law | 解釋為什麼先用小專案 |
| 16 | Continuous drift | 延伸到長期維護 |
| 17 | Open questions | 課程結尾討論 |

## 6. 文章每個點對應到本課程

| 文章點 | 課程階段 | 本專案檔案 |
| --- | --- | --- |
| Harness | Step 2 | 全 repo |
| Guides | Step 3 | `GUIDE.md` |
| Feedforward | Step 3 | `GUIDE.md` |
| Sensors | Step 4 | `harness/check.js`、`test/cart.test.js` |
| Feedback | Step 4-6 | `npm run harness` |
| Computational controls | Step 8 | Node test、自訂 check |
| Inferential controls | Step 8 | 講師 review、課堂討論 |
| Steering loop | Step 10 | 修改 guide 或 sensor |
| Keep quality left | Step 9 | commit 前跑 `npm run harness` |
| Maintainability harness | Step 7 | DOM 邊界檢查 |
| Architecture fitness harness | Step 6 | `cart.js` / `app.js` 分層 |
| Behaviour harness | Step 5 | 折扣與運費測試 |
| Harnessability | Step 11 | `src/cart.js` 純函式 |
| Harness templates | Step 12 | repo 結構 |
| Human role | Step 13 | 講師與學員決策 |
| Context engineering | Step 14 | README、GUIDE、test、harness |
| Ambient affordances | Step 14 | 目錄與檔名 |
| Ashby's Law | Step 15 | 小專案降低 variety |
| Continuous drift | Step 16 | 延伸 sensor |
| Open questions | Step 17 | 收尾討論 |
| Metaphors only go so far | Step 4 | sensor-pass 不等於絕對正確 |

## 7. 講師示範指令

啟動網站：

```bash
npm start
```

跑完整 harness：

```bash
npm run harness
```

只跑 behaviour tests：

```bash
npm test
```

只跑自訂 sensor：

```bash
node harness/check.js
```

## 8. 三個課堂破壞實驗

### 實驗 1：破壞行為

改：

```js
export const FREE_SHIPPING_THRESHOLD = 1000;
```

成：

```js
export const FREE_SHIPPING_THRESHOLD = 900;
```

預期：

- `npm test` 失敗。
- 引出 behaviour harness。

### 實驗 2：破壞架構

在 `src/cart.js` 加：

```js
document.querySelector("#cart-items");
```

預期：

- `harness/check.js` 失敗。
- 引出 architecture fitness harness。

### 實驗 3：破壞 guide 完整性

從 `README.md` 的原文元件表中刪掉 `Steering loop`。

預期：

- `harness/check.js` 失敗。
- 引出「harness 也可以檢查教材是否漏掉文章概念」。

## 9. 學員作業

請學員選自己的專案，填下表：

| 常見 agent 錯誤 | Guide 怎麼預防 | Sensor 怎麼檢查 | Computational 還是 Inferential |
| --- | --- | --- | --- |
| 例：忘記補測試 | AGENTS.md 寫新功能需測試 | coverage / test naming sensor | Computational |
| 例：誤解需求 | product spec 寫範例 | human review / AI review | Inferential |

最後請學員回答：

> 哪一個 sensor 最便宜、最適合下週就加到專案？

## 10. 一句話總結

> Harness Engineering 是一個循環：先用 guides 提高第一次做對的機率，再用 sensors 提供可修正的 feedback，最後由人類根據重複錯誤持續改進 harness。
