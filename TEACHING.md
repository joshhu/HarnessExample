# Harness Engineering 教學 Runbook

本文件是講師上課用的主流程。  
請不要把這堂課教成「小電商網站實作」，也不要一開始就丟一堆名詞。

這堂課真正要教的是：

> 當團隊使用 coding agent 時，如何用 guides 和 sensors 建立一個外層控制系統，讓 agent 在修改前被引導、修改後被檢查，並讓人類能持續改進這個控制系統。

本 repo 的小電商網站只是教具。  
網站越小越好，因為學員才看得見 Harness Engineering 本身。

## 課程設計原則

### 不要照文章順序教

原文是概念文章，適合讀；課堂要用體驗順序。

教學順序應該是：

1. 看到一個可理解的小系統。
2. 感受到 coding agent 可能犯錯。
3. 看到修改前的 guide。
4. 看到修改後的 sensor。
5. 故意破壞，讓 feedback 變具體。
6. 再把經驗對應回文章概念。

### 每次只引入一個概念

錯誤示範：

> Harness 有 feedforward、feedback、computational、inferential、regulation categories、harnessability...

正確節奏：

> 先看 `GUIDE.md`。這就是 guide。它在動手前發生，所以叫 feedforward。

### 講師要一直重複一句話

> Harness 不是工具清單；Harness 是一套讓 agent 比較不容易偏離目標的工程控制系統。

## 課程全貌

建議時長：90 分鐘。

| 段落 | 時間 | 教學焦點 | 引出的文章概念 |
| --- | --- | --- | --- |
| 1 | 0-10 分 | 看見小網站與可觀察行為 | 還不講名詞 |
| 2 | 10-20 分 | 討論 agent 會犯什麼錯 | trust barrier、user harness |
| 3 | 20-30 分 | 修改前先看 `GUIDE.md` | Guide、Feedforward |
| 4 | 30-40 分 | 修改後跑 `npm run harness` | Sensor、Feedback |
| 5 | 40-55 分 | 故意破壞購物車規格 | Behaviour harness |
| 6 | 55-65 分 | 故意破壞檔案邊界 | Architecture fitness、Maintainability |
| 7 | 65-75 分 | 分辨 deterministic 與語意判斷 | Computational、Inferential |
| 8 | 75-82 分 | 討論檢查放在哪個時間點 | Keep quality left、drift sensors |
| 9 | 82-90 分 | 把重複錯誤轉成 harness 改進 | Steering loop、Human role |

如果只有 45 分鐘，保留段落 1、2、3、4、5、9。

## 課前準備

在專案根目錄執行：

```bash
npm install
npm run harness
```

應看到：

```text
[harness-pass] guide, article checklist, and architecture boundaries passed
tests 7
pass 7
```

啟動網站：

```bash
npm start
```

開啟：

```text
http://localhost:4173
```

如果你要現場示範破壞程式，請先確認 git 是乾淨的：

```bash
git status --short
```

## 段落 1：先看網站，不講名詞

### 目的

建立所有學員都看得懂的共同情境。

這一段不要講 harness、guide、sensor。  
先讓學員知道這個系統「應該做什麼」。

### 講師操作

打開網站：

```text
http://localhost:4173
```

操作：

1. 點「通勤背包」。
2. 點「保溫杯」。
3. 指出畫面上的結果：
   - 小計：NT$1,200
   - 折扣：-NT$120
   - 運費：NT$0
   - 總金額：NT$1,080

### 講師台詞

> 這是一個很小的電商網站。使用者可以加商品、套折扣碼、看運費和總金額。今天我們不是要學怎麼寫電商，而是用這個簡單例子討論：如果請 coding agent 修改這個系統，我們要怎麼提高信心？

### 學員應該得到的理解

- 這個系統很小。
- 行為肉眼可見。
- 等一下所有 harness 概念都會綁回這些行為。

### 不要在這裡做的事

- 不要打開 `harness/check.js`。
- 不要講文章所有名詞。
- 不要解釋測試框架。

## 段落 2：先列出 agent 風險

### 目的

讓學員先感覺到「為什麼需要 harness」。

### 講師提問

> 如果我請 coding agent 幫這個網站新增功能或修 bug，你最怕它做錯什麼？

把答案寫在白板上。

常見答案：

```text
折扣算錯
免運門檻改錯
總金額算錯
UI 看起來正常但邏輯壞掉
把畫面操作寫進商業邏輯
忘記補測試
文件和程式不一致
改太多不相關的東西
```

### 講師台詞

> 這些擔心，就是文章一開始說的 trust barrier。LLM 不是 deterministic 的，它不一定知道我們的上下文，也不是真的理解整個系統。所以我們不能只靠最後人工 review。我們需要一個外層控制系統。

### 這裡才引出第一個詞：Harness

板書：

```text
Harness = agent model 外面的一層工程控制系統
```

講師補一句：

> 在這堂課，harness 不是某一個工具，而是 guide、sensor、測試、文件、流程和人類決策加起來。

### 對應原文

原文說 user harness 的目的有兩個：

- 提高 agent 第一次做對的機率。
- 在結果到人類眼前前，先提供自我修正的 feedback loop。

### 學員應該得到的理解

Harness 的需求來自風險，不是來自工具流行。

## 段落 3：Guide 是修改前的控制

### 目的

用 `GUIDE.md` 具體說明 guide 和 feedforward。

### 講師操作

打開：

```bash
open GUIDE.md
```

帶學員看三塊：

1. 產品規格。
2. 架構規則。
3. 講師故意破壞示範。

### 講師台詞

> 這份檔案是在 agent 或工程師動手前看的。它不是測試，它還沒有檢查任何結果。它的角色是先把方向講清楚，降低一開始走錯路的機率。

板書：

```text
Guide = 修改前的指引
Feedforward = 在錯誤發生前先引導
```

### 對應本專案

```text
GUIDE.md
```

它告訴 agent：

- 折扣碼是 `HARNESS10`。
- 折扣是 10%。
- 滿 NT$1,000 免運。
- `src/cart.js` 不能操作 DOM。
- `src/app.js` 才負責畫面互動。

### 講師提問

> 如果沒有這份 guide，agent 可能會問錯什麼、猜錯什麼、或放錯檔案？

預期回答：

- 不知道折扣規格。
- 不知道免運門檻。
- 不知道商業邏輯和畫面要分開。

### 對應原文

原文把 guides 稱為 feedforward controls：anticipate the agent's behaviour and steer it before it acts。

### 學員應該得到的理解

Guide 的價值不是「文件比較完整」，而是「修改前降低錯誤機率」。

## 段落 4：Sensor 是修改後的控制

### 目的

用 `npm run harness` 具體說明 sensor 和 feedback。

### 講師操作

執行：

```bash
npm run harness
```

### 預期輸出

```text
[harness-pass] guide, article checklist, and architecture boundaries passed
tests 7
pass 7
```

### 講師台詞

> 光有 guide 不夠。agent 讀了規則還是可能犯錯。所以我們需要在修改後觀察結果，這就是 sensor。sensor 給回饋，讓 agent 或工程師可以修正。

板書：

```text
Sensor = 修改後的檢查
Feedback = 觀察結果，指出偏差
```

### 對應本專案

```text
harness/check.js      自訂 sensor
test/cart.test.js     行為 sensor
npm run harness       一次跑完整 feedback
```

### `npm run harness` 做什麼

```text
node harness/check.js && npm test
```

第一段檢查：

- README 是否提到文章每個重要概念。
- `GUIDE.md` 是否明確說自己是 feedforward guide。
- HTML 是否用 `type="module"`。
- `src/cart.js` 是否保持純商業邏輯，不碰 DOM。

第二段檢查：

- 加商品後小計正確。
- 折扣碼正確。
- 免運門檻正確。
- 總金額正確。
- 金額格式正確。

### 重要提醒

講師一定要講這句：

> sensor-pass 不代表系統絕對正確，只代表目前這組 sensors 沒有看到問題。

這對應原文 sidebar：Metaphors only go so far。

### 學員應該得到的理解

Feedback 必須是可行動的訊號。  
只是說「有 bug」不夠，最好能指出違反哪條規則。

## 段落 5：第一次破壞，示範 Behaviour Harness

### 目的

讓學員親眼看到 sensor 失敗。  
這比抽象解釋 behaviour harness 有效。

### 講師操作

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

### 預期觀察

測試會失敗，因為規格是滿 NT$1,000 免運，不是滿 NT$900。

### 講師台詞

> 這次失敗不是程式格式問題，也不是架構問題，而是使用者看得見的行為錯了。這就是 behaviour harness 的範圍。

板書：

```text
Behaviour harness = 保護使用者需要的功能行為
```

### 對應本專案

```text
GUIDE.md              behaviour 的 feedforward
test/cart.test.js     behaviour 的 feedback
```

### 對應原文

原文說 behaviour harness 是最難的一塊，因為：

- 功能規格可能不清楚。
- AI 產生的測試不一定可信。
- 很多行為仍需要人工測試或 approved fixtures。

### 講師補充 approved fixtures

這裡可以補一句：

> 在真實專案中，我們不應只相信 agent 自己寫的測試。像這個案例裡，「通勤背包 + 保溫杯 = NT$1,200，折扣後 NT$1,080」可以當成講師批准的 fixture。

### 修回程式

把門檻改回：

```js
export const FREE_SHIPPING_THRESHOLD = 1000;
```

再跑：

```bash
npm run harness
```

## 段落 6：第二次破壞，示範 Architecture Fitness Harness

### 目的

讓學員看到：不是只有功能錯誤需要 feedback，架構邊界也需要 feedback。

### 講師操作

在 `src/cart.js` 最下面暫時加入：

```js
document.querySelector("#cart-items");
```

執行：

```bash
npm run harness
```

### 預期輸出

```text
[harness-fail] src/cart.js must stay pure and must not touch DOM APIs
```

### 講師台詞

> 這次購物車金額不一定會錯，但架構已經壞了。`cart.js` 應該只做商業邏輯，DOM 操作應該留在 `app.js`。這種檢查就是 architecture fitness harness。

板書：

```text
Architecture fitness harness = 保護系統的架構特性
```

### 對應本專案

```text
GUIDE.md          架構 guide
harness/check.js  架構 sensor
src/cart.js       商業邏輯
src/app.js        UI glue
```

### 對應原文

原文把這類檢查連到 fitness functions：定義並檢查應用程式的架構特性。

### 修回程式

移除剛剛新增的：

```js
document.querySelector("#cart-items");
```

## 段落 7：同一個例子引出 Maintainability Harness

### 目的

說明 maintainability harness 與 architecture fitness harness 有時會重疊，但關注點不同。

### 講師台詞

> 剛剛 `cart.js` 不准碰 DOM，也可以從 maintainability 的角度理解。商業邏輯和畫面混在一起，短期可能能跑，長期會難測、難改、難讓 agent 理解。

板書：

```text
Maintainability harness = 保護程式可讀、可測、可改
```

### 本專案的 maintainability sensor

`harness/check.js` 禁止 `cart.js` 出現：

```text
document.
querySelector
innerHTML
addEventListener
```

### 真實專案可能使用

```text
ESLint
TypeScript
coverage
duplicate code detector
complexity checker
dependency scanner
```

### 對應原文

原文指出 maintainability harness 目前最容易做，因為已有很多成熟 deterministic 工具。

## 段落 8：Computational vs Inferential

### 目的

學員已經看過測試與 sensor，現在可以分類。

### 講師板書

```text
Computational = CPU 可穩定執行，快、便宜、可重複
Inferential   = 需要語意推論，慢、較貴、較不穩定
```

### 本專案分類

| 控制 | 類型 | 原因 |
| --- | --- | --- |
| `node --test` | Computational sensor | deterministic 測試 |
| `harness/check.js` | Computational sensor | 固定規則掃描 |
| `GUIDE.md` | Feedforward guide | 修改前引導 |
| 講師問答 | Inferential feedback | 需要語意判斷 |
| 判斷是否過度設計 | Inferential | 很難靠固定規則判斷 |

### 講師提問

> 檢查總金額是不是 NT$1,080，適合 computational 還是 inferential？

答案：Computational。

> 判斷 agent 的解法是不是過度設計，適合 computational 還是 inferential？

答案：Inferential。

### 對應原文

原文說 computational controls 快又可靠，適合每次變更都跑；inferential controls 能處理語意，但較慢、較貴、較不 deterministic。

## 段落 9：Keep Quality Left

### 目的

讓學員知道 sensors 不只要有，還要放對時間點。

### 講師板書

```text
越早發現，越便宜

修改前：GUIDE.md
修改後：npm run harness
PR 前：human / AI review
CI：重跑 sensors
長期：drift / health sensors
```

### 講師台詞

> `npm run harness` 不應該等到最後才跑。它應該在 commit 前、甚至 agent 每次修改後就跑。這就是 keep quality left。

### 對應原文

原文把 feedback sensors 分散到 change lifecycle：

- 便宜快速的放越左邊。
- 昂貴的放到 pipeline 或 integration 後。
- 漸進腐化的問題用 continuous sensors。

### 本專案現況

目前只有最左側的本機 harness：

```bash
npm run harness
```

可延伸：

```text
CI 每次 push 跑 npm run harness
每天跑 drift sensor
定期檢查 README 規格與 cart.js 常數是否一致
```

## 段落 10：Continuous Drift 與 Health Sensors

### 目的

補足原文 timing 章節中「不是每個問題都跟單次 change 綁在一起」的觀念。

### 講師台詞

> 有些問題不是某一次改壞，而是慢慢壞掉。這種就需要 continuous drift 或 health sensors。

### 小電商例子

| 漂移問題 | 可以設計的 sensor |
| --- | --- |
| README 寫滿千免運，程式變成滿九百免運 | 文件與常數一致性檢查 |
| 測試只測 happy path | mutation testing 或 test quality review |
| guide 很久沒更新 | guide freshness check |
| 相依套件老化 | dependency scanner |
| 網站效能變慢 | lighthouse / runtime metric |

### 對應原文

原文提到 dead code detection、coverage quality、dependency scanners、runtime SLO、log anomalies。

## 段落 11：Steering Loop

### 目的

這是整堂課最重要的收斂：人類不是只修 code，而是修 harness。

### 講師提問

> 如果 agent 第一次把 DOM 寫進 `cart.js`，我們修 code。那如果第二次、第三次又發生，代表什麼？

預期答案：

> 代表 harness 不夠好。

### 講師板書

```text
第一次錯：修 code
第二次同類錯：修 guide 或 sensor
```

### 可操作示範

假設錯誤是「agent 常忘記金額要 NT$」。

問學員：

```text
要改 GUIDE.md 嗎？
要加 test 嗎？
要加 harness/check.js 規則嗎？
還是只需要人工 review？
```

### 對應原文

原文說 human 的工作是在 steering loop 中持續迭代 harness。  
AI 也可以協助產生 custom controls、static analysis、how-to guides。

### 學員應該得到的理解

Harness Engineering 的核心不是「跑測試」，而是：

> 把重複發生的錯誤轉成新的 guide 或 sensor。

## 段落 12：Human Role

### 目的

避免學員誤解成「有 harness 就不需要人」。

### 講師台詞

> Harness Engineering 不是把人類拿掉，而是把人類從重複檢查移到系統設計的位置。

### 人類負責

- 決定哪些行為重要。
- 決定哪些錯誤值得自動化檢查。
- 決定 guide 寫到什麼程度。
- 判斷 inferential 問題。
- 調整太弱或太吵的 sensors。
- 維護 harness 本身。

### 對應原文

原文圖中 human 同時 steering guides 和 sensors。

## 段落 13：Harnessability

### 目的

讓學員知道程式本身也要設計成容易被 harness 管。

### 講師台詞

> 不是所有程式都一樣容易被 harness。越混亂、越隱含狀態、越難測，agent 和 sensor 都越難工作。

### 本專案為什麼 harnessable

```text
src/cart.js   純商業邏輯，可直接測
src/app.js    DOM glue，不放商業規則
test/         可快速驗證行為
harness/      可快速檢查邊界
GUIDE.md      規格集中
```

### 反例

如果折扣、運費、DOM 操作全部寫在 `index.html` 裡：

- 測試難寫。
- sensor 難檢查。
- agent 容易亂改。
- 人類 review 成本提高。

### 對應原文

Harnessability 是系統是否容易被 harness 控制的能力。

## 段落 14：Harness Templates

### 目的

讓學員把本例帶回自己的專案，而不是只記得電商。

### 講師台詞

> 這個 repo 最有價值的不是購物車，而是它的形狀可以複製。

### 可複製模板

```text
GUIDE.md              修改前指引
src/                  可測的產品邏輯
test/                 behaviour feedback
harness/              專案自訂 sensors
npm run harness       單一入口
README.md             教學與概念地圖
```

### 套到其他網站

| 網站 | Behaviour harness |
| --- | --- |
| 報名網站 | 名額、費用、email 驗證 |
| 訂房網站 | 日期、房價、取消規則 |
| 會員網站 | 權限、登入狀態 |
| SaaS 後台 | 篩選、排序、權限、狀態轉換 |

## 段落 15：Context Engineering 與 Ambient Affordances

### 目的

補足原文 sidebars，讓學員知道 repo 結構和上下文也是 harness 的一部分。

### Context Engineering

講師台詞：

> Context engineering 是讓 agent 看得到該看的上下文。Harness engineering 則是把這些上下文和 feedback 組成控制系統。

本專案的 context：

```text
GUIDE.md
README.md
test/cart.test.js
harness/check.js
檔案命名
```

### Ambient Affordances

講師台詞：

> Ambient affordances 是環境本身給出的提示。清楚的資料夾和檔名會讓人和 agent 比較不容易做錯。

本專案例子：

```text
src/cart.js     看起來就是購物車邏輯
src/app.js      看起來就是畫面互動
test/           看起來就是測試
harness/        看起來就是自訂控制
```

講師提問：

> 如果檔案都叫 `main.js`、`helper.js`、`stuff.js`，agent 會更容易還是更不容易做對？

## 段落 16：Ashby's Law / Variety

### 目的

說明為什麼這個教學專案刻意很小。

### 講師台詞

> 控制系統要能處理被控制系統的變化。如果專案太大、規則太多、狀態太亂，簡單 harness 就管不住。

### 本課程的設計

我們刻意降低 variety：

```text
3 個商品
1 個折扣碼
1 個免運門檻
1 個商業邏輯檔
1 個自訂 sensor
7 個測試
```

講師說：

> 初學先用小例子看懂控制系統。回到真實專案後，再逐步擴大 harness。

## 段落 17：Open Questions

### 目的

讓學員知道 Harness Engineering 不是已經完全解決的標準答案。

### 討論題

1. 如果 `GUIDE.md` 和 `test/cart.test.js` 寫的不一致，agent 該相信誰？
2. 如果 sensor 從來沒有失敗，是品質很好，還是 sensor 太弱？
3. 哪些錯誤值得變成 computational sensor？
4. 哪些錯誤只能留給 inferential review？
5. 誰負責維護 harness？
6. Harness 本身要不要 code review？
7. Sensor 太吵時，團隊會不會開始忽略它？

### 講師收尾

> Harness 本身也會老化。成熟團隊不是一次把 harness 寫完，而是持續觀察 agent 和工程師的錯誤，把重複錯誤轉成新的 guide 或 sensor。

## 一頁式原文對照表

| 原文概念 | 這堂課何時講 | 本專案對應 |
| --- | --- | --- |
| Harness | 段落 2 | 整個 repo |
| Guide | 段落 3 | `GUIDE.md` |
| Sensor | 段落 4 | `harness/check.js`、`test/cart.test.js` |
| Feedforward | 段落 3 | 修改前讀 guide |
| Feedback | 段落 4-6 | `npm run harness` |
| Computational | 段落 8 | Node test、自訂 sensor |
| Inferential | 段落 8 | 講師 review、學員討論 |
| Steering loop | 段落 11 | 同類錯誤重複時改 guide/sensor |
| Keep quality left | 段落 9 | commit 前跑 harness |
| Continuous drift | 段落 10 | 延伸的長期 sensors |
| Maintainability harness | 段落 7 | 禁止 `cart.js` 操作 DOM |
| Architecture fitness harness | 段落 6 | `cart.js` / `app.js` 邊界 |
| Behaviour harness | 段落 5 | 折扣與運費測試 |
| Harnessability | 段落 13 | 純商業邏輯與可測結構 |
| Harness templates | 段落 14 | `GUIDE.md` + `test/` + `harness/` |
| Human role | 段落 12 | 人類 steering harness |
| Context engineering | 段落 15 | 提供 agent 需要的上下文 |
| Ambient affordances | 段落 15 | 清楚檔名與資料夾 |
| Ashby's Law | 段落 16 | 降低教學專案 variety |
| Metaphors only go so far | 段落 4 | sensor-pass 不等於絕對正確 |
| Open questions | 段落 17 | 結尾討論 |

## 45 分鐘壓縮版

如果時間只有 45 分鐘，照這樣教：

1. 0-5 分：看網站。
2. 5-10 分：問 agent 會犯什麼錯。
3. 10-18 分：看 `GUIDE.md`，講 guide / feedforward。
4. 18-25 分：跑 `npm run harness`，講 sensor / feedback。
5. 25-32 分：改壞免運門檻，講 behaviour harness。
6. 32-38 分：讓 `cart.js` 碰 DOM，講 architecture fitness。
7. 38-45 分：用 steering loop 收尾。

## 120 分鐘工作坊版

如果有 120 分鐘，加入學員實作：

### 實作 1：新增 behaviour 規格

需求：

> 新增折扣碼 `VIP50`，固定折 NT$50。

學員要做：

- 更新 `GUIDE.md`。
- 更新 `src/cart.js`。
- 更新 `test/cart.test.js`。
- 跑 `npm run harness`。

討論：

- 哪個是 feedforward？
- 哪個是 feedback？
- 哪個是 behaviour harness？

### 實作 2：新增一個自訂 sensor

需求：

> 禁止 README 遺漏 `Keep quality left`。

學員要做：

- 看 `harness/check.js`。
- 新增 required concept。
- 故意刪 README 文字。
- 確認 sensor 失敗。

討論：

- 這個 sensor 有沒有太表面？
- 它保護的是產品品質，還是教材完整性？

### 實作 3：設計自己的 harness

請學員填：

| 自己專案的常見錯誤 | Guide | Sensor | Computational / Inferential |
| --- | --- | --- | --- |
| | | | |

## 最後一句話

> Harness Engineering 的教學重點不是讓學生記名詞，而是讓他們經歷一次循環：先用 guide 引導，再用 sensor 回饋，最後由人類把重複錯誤轉成更好的 harness。
