# Harness Engineering 完整教學手冊

本手冊是講師用教材，目標不是只介紹一個範例專案，而是讓你可以清楚說明 Martin Fowler 網站文章
[Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
中的每個核心元件，並把每個元件對應到本專案的文件、程式、測試與課堂活動。

這份教材的定位：

- 你可以照著本手冊講一堂 3 小時工作坊。
- 你可以用本專案示範「為 coding agent 建立工程控制系統」。
- 學員不需要先懂 Harness Engineering，也能從儀器軟體情境理解。
- 每個原文概念都會回答三件事：
  - 這是什麼？
  - 在儀器軟體中為什麼重要？
  - 在本專案中對應到哪個檔案與哪個示範？

## 0. 課前給講師的總覽

### 這堂課到底在教什麼？

這堂課不是在教「怎麼寫一個光譜儀校正程式」。

這堂課真正要教的是：

> 當團隊開始使用 coding agent 時，不能只靠人類事後 review。你要把資深工程師腦中的經驗、規格、架構邊界、測試習慣、常見錯誤，外顯成 guides 與 sensors，讓 coding agent 在做事前被引導，做事後被檢查，並在錯誤送到人類前先修正。

原文把這套外層控制系統稱為 harness。

### 為什麼用儀器公司當案例？

儀器軟體很適合教 Harness Engineering，因為它同時有下列特徵：

- 硬體行為可能不穩定，但軟體測試必須可重現。
- 校正結果有明確驗收條件，不能只靠「看起來差不多」。
- 架構邊界很重要，演算法、硬體 I/O、CLI、資料格式混在一起會很難驗證。
- 品質問題發現太晚時，成本很高，甚至會影響交機、維修與客戶信任。
- 資深工程師常有大量隱性知識，剛好可以轉成 guides 與 sensors。

### 本專案的故事

我們假設有一套「光譜儀濃度校正服務」：

1. 儀器掃描一組標準品。
2. 軟體取得濃度與儀器讀值。
3. 軟體用線性校正模型建立校正曲線。
4. 軟體輸出校正憑證。
5. 系統判斷本次校正是否通過。

這個故事很小，但足以示範所有 Harness Engineering 元件。

## 1. 原文核心觀念總表

| 原文元件 | 一句話解釋 | 本專案對應 |
| --- | --- | --- |
| Harness | 圍繞 coding agent 的外層工程控制系統 | 整個 repo：guides、sensors、tests、CLI、docs |
| Guide | 修改前的指引，屬於 feedforward | `AGENTS.md`、`guides/*.md` |
| Sensor | 修改後的檢查與回饋，屬於 feedback | `harness-sensors`、pytest、coverage、ruff |
| Feedforward | 事情發生前先降低錯誤機率 | 先讀規格、架構規則、agent guide |
| Feedback | 事情發生後觀察結果並修正 | 測試失敗、sensor 失敗、coverage 不足 |
| Computational control | deterministic、快速、可重複的控制 | AST sensor、unit tests、coverage、ruff |
| Inferential control | 需要語意判斷的控制 | `guides/inferential-review.md` |
| Steering loop | 人類根據回饋調整 guide 或 sensor | 課堂練習三 |
| Keep quality left | 讓品質問題提早出現 | commit 前跑 `uv run harness-sensors --with-tests` |
| Maintainability harness | 維持可讀性、可維護性 | `maintainability_sensor.py`、ruff、coverage |
| Architecture fitness harness | 維持架構特性 | `architecture_sensor.py`、`guides/architecture.md` |
| Behaviour harness | 確認行為符合需求 | `tests/test_calibration_behaviour.py`、`guides/product-spec.md` |
| Harnessability | 程式是否容易被 harness 管理 | 純函式校正、分層模組、deterministic fixture |
| Harness template | 可複製的 harness 樣板 | 本 repo 結構可複製到其他儀器專案 |
| Human role | 人類仍負責目標、取捨與判斷 | 講師 review、規格決策、sensor 強化 |
| Variety / Ashby | 控制系統的複雜度要能匹配被控制系統 | 限定小範圍案例，讓 harness 足以治理 |

## 2. 課程主軸：不要把 agent 當神，要把 agent 放進控制系統

### 講師要講的重點

很多人使用 coding agent 的方式是：

1. 給一個需求。
2. 等 agent 產生程式。
3. 人類 review。
4. 發現問題後再改 prompt。

這種方式會讓人類變成最後一道防線，壓力很大，也很難規模化。

Harness Engineering 的想法是把流程改成：

1. 修改前：用 guides 告訴 agent 規格、架構、限制、範例。
2. 修改中：讓 agent 在可理解的專案結構裡工作。
3. 修改後：用 sensors 給明確 feedback。
4. 若錯誤重複發生：人類更新 guides 或 sensors。

### 板書圖

```text
                 feedforward
     +--------------------------------+
     | guides / examples / standards |
     +--------------------------------+
                     |
                     v
    human goal -> coding agent -> code change
                     |
                     v
     +--------------------------------+
     | tests / linters / sensors      |
     +--------------------------------+
                 feedback
                     |
                     v
             human steering loop
```

### 本專案怎麼示範

先讓學員看到「產品功能」：

```bash
uv run instrument-lab calibrate --fixture stable
```

再讓學員看到「外層控制」：

```bash
uv run harness-sensors --with-tests
```

你要強調：第二個指令才是這堂課的主角。產品程式只是被 harness 管理的對象。

## 3. Harness：外層工程控制系統

### 原文概念

Harness 不是單一工具，不是某個測試框架，也不是 prompt。它是一整組圍繞 coding agent 的控制系統，包含規格、文件、範例、測試、檢查器、review 流程與人類決策。

### 儀器軟體中的意義

儀器公司常有很多「大家心裡知道但文件沒寫」的規則，例如：

- 校正資料要可追溯。
- 測試不能依賴真實硬體。
- 演算法不可直接做 UI 輸出。
- 儀器讀值 fixture 要 deterministic。
- 驗收門檻變更時要同步更新文件、測試與 CLI。

這些規則如果只放在資深工程師腦中，coding agent 不會知道，新進工程師也不容易知道。

Harness 的任務就是把這些規則外顯。

### 本專案對應

整個 repo 就是一個 harness：

```text
AGENTS.md                         修改前的 agent guide
guides/product-spec.md            行為規格 guide
guides/architecture.md            架構 guide
guides/inferential-review.md      語意 review guide
src/instrument_harness_lab/       被管理的產品程式
src/.../sensors/                  feedback sensors
tests/                            behaviour feedback
docs/                             講師與設計文件
```

### 講師示範方式

先不要一開始就打開程式碼。先問學員：

> 如果你請 coding agent 幫你改一個儀器校正功能，你最擔心它犯什麼錯？

把學員回答寫到白板，通常會有：

- 規格理解錯。
- 測試沒補。
- 硬體行為亂模擬。
- 把功能寫在錯的層。
- 看起來通過，但數學上不合理。

接著說：這些擔心都可以被轉成 harness 的某個元件。

## 4. Guides：修改前的 feedforward 控制

### 原文概念

Guide 是在 agent 或工程師動手前提供的指引。它不保證一定正確，但可以降低一開始走錯方向的機率。

Guide 常見形式：

- 專案規則。
- 架構文件。
- 產品規格。
- 範例。
- prompt template。
- review checklist。
- coding standard。

### 本專案有哪些 guides？

#### 4.1 `AGENTS.md`

這是最上層 guide，回答「agent 在這個 repo 工作前必須知道什麼」。

重點內容：

- 使用繁體中文台灣用語。
- Python 使用 `uv`。
- 儀器模擬必須 deterministic。
- 模組邊界。
- 每個新功能都要有測試。
- 同一類錯誤出現第二次，要新增或更新 guide 或 sensor。

講師講法：

> AGENTS.md 就像是你把資深工程師帶新人的第一天交代，寫成 agent 讀得懂的文件。它不是產品規格，而是工作方式規格。

#### 4.2 `guides/product-spec.md`

這是 behaviour guide，回答「校正功能應該做什麼」。

它定義：

- 輸入：標準濃度與儀器讀值。
- 演算法：一次線性迴歸。
- 輸出：係數、R²、最大誤差、accepted、各點誤差。
- 驗收條件：
  - `r_squared >= 0.995`
  - `max_absolute_error <= 1.5`

講師講法：

> 這份文件的價值不是寫給客戶看，而是讓 agent 在寫 code 前知道什麼叫做通過。

#### 4.3 `guides/architecture.md`

這是 architecture fitness guide，回答「功能應該放在哪裡」。

它規定：

```text
domain      <- calibration
domain      <- instrument
domain      <- controller
instrument  <- controller
calibration <- controller
controller  <- cli
```

講師講法：

> 這張依賴圖就是防止 agent 把校正演算法、硬體模擬與 CLI 輸出全部塞在一起。

#### 4.4 `guides/inferential-review.md`

這是 inferential review guide，回答「哪些事情 deterministic 工具不一定抓得到」。

範例：

- 程式是否符合儀器軟體語意？
- 是否把領域知識藏在 CLI？
- 是否過度設計？
- 是否需要新增新的 guide 或 sensor？

講師講法：

> 不是所有品質都能靠 AST 或 unit test 抓到。有些事情需要語意判斷，這就是 inferential control 的位置。

## 5. Feedforward：在錯誤發生前先引導

### 原文概念

Feedforward 是控制理論中的概念：在系統輸出錯誤前，先根據已知資訊調整輸入。

放在 coding agent 情境，就是在 agent 開始改程式前，先提供：

- 規格。
- 範例。
- 架構邊界。
- 禁止事項。
- 測試方式。
- 常見錯誤。

### 儀器軟體中的意義

假設你只跟 agent 說：

> 幫我加一個校正功能。

agent 可能會：

- 寫出不能追溯每個標準點誤差的程式。
- 用不可重現亂數模擬儀器。
- 把 `print` 放在演算法中。
- 忘記 rejected case。

如果你先提供 guide，agent 比較可能第一次就做對。

### 課堂示範

請學員打開：

```bash
open AGENTS.md
open guides/product-spec.md
open guides/architecture.md
```

然後問：

> 如果沒有這三份 guide，agent 最可能犯哪三種錯？

預期答案：

- 不知道驗收條件。
- 不知道模組邊界。
- 不知道工具與測試規則。

## 6. Sensors：修改後的 feedback 控制

### 原文概念

Sensor 是在 agent 產生結果後觀察系統狀態的東西。它把「程式有沒有偏離目標」轉成可行動的訊號。

Sensor 可以是：

- unit tests。
- end-to-end tests。
- linter。
- static analysis。
- coverage。
- architecture fitness function。
- security scan。
- AI reviewer。

### 本專案有哪些 sensors？

#### 6.1 `uv run ruff check .`

檢查格式與基本 Python 程式問題。

它屬於：

- feedback
- computational control
- maintainability harness

#### 6.2 `uv run pytest`

檢查行為是否符合規格。

它屬於：

- feedback
- computational control
- behaviour harness

#### 6.3 `uv run pytest --cov=instrument_harness_lab --cov-report=term-missing`

檢查測試覆蓋率是否維持在 90% 以上。

它屬於：

- feedback
- computational control
- maintainability harness

#### 6.4 `uv run harness-sensors`

執行專案自訂 sensors：

- architecture sensor
- maintainability sensor

#### 6.5 `uv run harness-sensors --with-tests`

執行自訂 sensors 加 pytest，是課堂建議的主要品質門檻。

### 講師示範

```bash
uv run harness-sensors --with-tests
```

你要解釋：

> sensor-pass 不是說軟體完美，而是說目前這組 harness 沒有觀測到違規。這句話很重要，因為 harness 不是魔法，它只會抓你明確設計要抓的偏差。

## 7. Feedback：讓 agent 有機會自我修正

### 原文概念

Feedback 是在結果產生後，把結果跟目標比較，然後把偏差傳回系統。

在 coding agent 流程中，好的 feedback 必須：

- 夠快。
- 訊息清楚。
- 可重複。
- 指向可修正的行動。

### 不好的 feedback

```text
Test failed.
```

太模糊。

### 較好的 feedback

```text
[sensor-fail] calibration.py must not import instrument_harness_lab.cli
```

這種訊息指出：

- 哪裡錯。
- 違反哪條規則。
- agent 應該往哪個方向修。

### 本專案示範

你可以在課堂中故意破壞架構：

1. 打開 `src/instrument_harness_lab/calibration.py`。
2. 加入錯誤 import：

```python
from instrument_harness_lab.cli import main
```

3. 執行：

```bash
uv run harness-sensors
```

4. 讓學員觀察 architecture sensor 的錯誤。

課堂重點：

> feedback 不是罵人，它是讓系統知道自己偏離哪個控制範圍。

## 8. Computational Controls：快速、可重複、明確

### 原文概念

Computational control 是可以由程式 deterministic 執行的控制。它通常便宜、快速、穩定，因此適合頻繁執行。

### 本專案 computational controls

| 控制 | 檔案或指令 | 檢查內容 |
| --- | --- | --- |
| ruff | `uv run ruff check .` | Python 風格與基本問題 |
| pytest | `uv run pytest` | 行為規格 |
| coverage | `--cov` | 測試保護範圍 |
| architecture sensor | `architecture_sensor.py` | 模組依賴方向 |
| maintainability sensor | `maintainability_sensor.py` | 函式長度、分支、輸出邊界 |

### 講師講法

> 能用 computational sensor 抓的問題，不要每次都交給人類 review。人類 review 應該處理語意、取捨、風險，而不是重複抓同一種低階錯誤。

## 9. Inferential Controls：語意判斷與不確定性

### 原文概念

Inferential control 不是用固定規則判斷，而是需要推論與語意理解。它可能由人類、LLM reviewer 或更高階工具執行。

### 儀器軟體中的例子

以下問題不一定能被 deterministic sensor 抓到：

- 校正模型雖然通過測試，但是否符合實際儀器物理特性？
- 新增 fixture 的資料是否看起來合理？
- 錯誤訊息是否能幫助維修工程師追查問題？
- 這個抽象是否過度設計？
- 這次變更是否讓未來接實體儀器更困難？

### 本專案對應

檔案：

```text
guides/inferential-review.md
```

它提供 reviewer prompt/checklist。

### 講師示範方式

你可以在課堂中問：

> 為什麼我們沒有把 inferential review 寫成預設必跑？

答案：

- 它可能需要 API key。
- 成本較高。
- 結果可能不穩定。
- 它適合補足 deterministic sensor，不適合取代 deterministic sensor。

## 10. Steering Loop：人類如何調整 harness

### 原文概念

Steering loop 是 Harness Engineering 的關鍵。人類不只是 review agent 產出的程式，而是觀察 agent 常犯的錯，然後改進 guides 或 sensors。

### 核心口訣

> 同一種錯誤第一次出現，可以修 code；第二次出現，就應該考慮修 harness。

### 課堂練習

讓學員分組完成：

1. 故意新增一個錯誤。
2. 看 sensor 是否抓得到。
3. 如果抓不到，新增 guide 或 sensor。
4. 說明這個新增控制屬於哪一類。

### 範例

情境：學員一直忘記讓 fixture deterministic。

可新增 guide：

```text
所有 fixture 必須固定 seed，不得使用 random.random() 的全域狀態。
```

可新增 sensor：

```text
掃描 src/ 中是否直接使用 random.random()。
```

討論：

- guide 是 feedforward。
- sensor 是 feedback。
- AST 掃描是 computational。
- 判斷 fixture 是否符合真實儀器風險可能是 inferential。

## 11. Keep Quality Left：品質往左移

### 原文概念

Keep quality left 的意思是讓品質檢查盡量提早發生。不要等到 PR review、QA、現場測試或客戶抱怨才發現問題。

### 在本專案中的實作

課堂建議每次修改後都跑：

```bash
uv run harness-sensors --with-tests
```

這個指令代表 commit 前品質門檻。

### 儀器公司情境

品質問題越晚發現越貴：

| 發現時間 | 成本 |
| --- | --- |
| 寫 code 當下 | 低 |
| commit 前 | 低 |
| PR review | 中 |
| CI | 中 |
| 接實體儀器後 | 高 |
| 客戶現場 | 很高 |

講師講法：

> Harness Engineering 的價值不是讓錯誤永遠不發生，而是把錯誤從右邊拉回左邊。

## 12. 三種 Regulation Categories

原文把 harness 的應用分成幾種調節類型。本專案全部都有示範。

### 12.1 Maintainability Harness

目標：

- 程式容易讀。
- 程式容易測。
- 程式不過度複雜。
- 人類與 agent 都能理解。

本專案對應：

```text
src/instrument_harness_lab/sensors/maintainability_sensor.py
uv run ruff check .
coverage 90% 門檻
```

檢查內容：

- 函式不能太長。
- 分支不能太複雜。
- 除了 CLI 與 sensor runner，其他模組不能直接 `print`。

講師講法：

> 儀器軟體會長期維護，交機後還會有維修、校正規格變更、硬體 revision。可維護性不是美觀問題，是成本問題。

### 12.2 Architecture Fitness Harness

目標：

- 維持架構特性。
- 防止依賴方向慢慢腐敗。
- 讓演算法保持可測。

本專案對應：

```text
guides/architecture.md
src/instrument_harness_lab/sensors/architecture_sensor.py
```

模組角色：

| 模組 | 責任 |
| --- | --- |
| `domain.py` | 資料模型 |
| `instrument.py` | 儀器 fixture 與模擬 |
| `calibration.py` | 校正演算法 |
| `controller.py` | 流程編排 |
| `cli.py` | 使用者輸出 |

講師講法：

> 架構不是畫圖用的。architecture fitness harness 會把圖變成可以執行的檢查。

### 12.3 Behaviour Harness

目標：

- 確認系統行為符合使用者故事。
- 規格變更時，測試能提醒你同步修改。

本專案對應：

```text
guides/product-spec.md
tests/test_calibration_behaviour.py
```

測試保證：

- `stable` fixture 必須 accepted。
- `drifted` fixture 必須 rejected。
- 校正結果必須保留每個標準點的誤差。
- 錯誤輸入要有清楚例外。

講師講法：

> Behaviour harness 不是測函式而已，它是在保護使用者故事。

## 13. Harnessability：讓程式本身容易被 harness 控制

### 原文概念

Harnessability 是指一個系統是否容易被 guides 與 sensors 管理。如果程式本身混亂、不可測、依賴隱藏狀態，再多 harness 也很難有效。

### 本專案如何提高 harnessability？

#### 13.1 校正演算法是純函式

檔案：

```text
src/instrument_harness_lab/calibration.py
```

`fit_linear_calibration()` 接收標準點，回傳結果，不讀檔、不印字、不碰硬體。

好處：

- 容易測。
- 容易重現。
- 容易被 agent 修改。
- sensor 容易判斷邊界。

#### 13.2 fixture deterministic

檔案：

```text
src/instrument_harness_lab/instrument.py
```

每個 fixture 都有固定 seed。

好處：

- 每次測試結果一致。
- 學員不會遇到偶發測試失敗。
- sensor feedback 可被信任。

#### 13.3 CLI 只負責輸出

檔案：

```text
src/instrument_harness_lab/cli.py
```

CLI 不直接做校正數學。

好處：

- 行為測試不用透過 CLI 才能測。
- 產品邏輯可以重用。
- 輸出格式與演算法分離。

### 講師講法

> Harnessability 是 agent 時代很重要的設計品質。你不是只設計給人類看，也是在設計給工具檢查、給 agent 理解。

## 14. Harness Templates：把這套方法複製到其他儀器專案

### 原文概念

Harness template 是可重複使用的 harness 樣板。不同專案不應每次從零開始想 guides 與 sensors。

### 本專案可複製的樣板

```text
AGENTS.md
guides/product-spec.md
guides/architecture.md
guides/inferential-review.md
src/<package>/sensors/
tests/test_*_behaviour.py
docs/TEACHING_MANUAL.md
```

### 可套用到哪些儀器？

- 溫控箱控制器。
- 幫浦流量校正。
- 光學量測儀。
- 資料擷取器。
- 半導體測試設備。
- 醫療檢測儀器。

### 套用步驟

1. 保留 `AGENTS.md` 的工具與品質規則。
2. 把 `product-spec.md` 改成該儀器的使用者故事與驗收條件。
3. 把 `architecture.md` 改成該系統的模組邊界。
4. 保留 `sensors/` 結構，替換檢查規則。
5. 建立一個 deterministic simulator 或 fixture。
6. 把「真實硬體測試」留給較晚層級，把 deterministic feedback 放在最左邊。

## 15. Variety / Ashby：控制系統要匹配被控制系統

### 原文概念

原文引用控制理論中的觀念：如果被控制系統可能出現很多變化，控制系統也需要足夠能力處理那些變化。

### 用白話講

如果你讓 agent 在一個巨大、混亂、沒有規格、沒有測試、沒有架構邊界的 repo 裡自由修改，那 harness 很難控制它。

如果你把工作切成小任務，並提供明確 guides 與 sensors，控制就容易很多。

### 本專案如何降低 variety？

- 只做一個光譜儀校正案例。
- 只用 deterministic fixture。
- 只用清楚分層的 5 個產品模組。
- 只設定少量但可執行的品質門檻。

講師講法：

> 一開始不要拿整個大型系統測 Harness Engineering。先從小而完整的切片開始，讓控制系統真的有效。

## 16. Human Role：人類沒有消失，人類負責 steering

### 原文概念

Harness Engineering 不是把人類拿掉，而是改變人類工作位置。人類不該一直做重複檢查，而要負責設定方向、更新控制、處理例外與做風險判斷。

### 在本專案中，人類負責什麼？

- 決定 R² 與最大誤差門檻。
- 判斷 fixture 是否符合真實儀器風險。
- 決定哪些 sensor 要放在 commit 前，哪些放在 CI。
- review inferential checklist。
- 當錯誤重複發生時，新增 guide 或 sensor。

### 講師講法

> 人類不是 agent 的打字機，也不是最後擦屁股的人。人類是控制系統的設計者。

## 17. 專案導覽：每個檔案在教什麼？

### `src/instrument_harness_lab/domain.py`

教學重點：

- 用資料模型清楚表達儀器領域語意。
- `StandardPoint`、`PointPrediction`、`CalibrationResult` 讓測試與 CLI 都能讀懂結果。

### `src/instrument_harness_lab/instrument.py`

教學重點：

- 實體硬體尚未接入前，用 deterministic simulator 建立 feedback。
- `stable` 與 `drifted` fixture 示範通過與失敗案例。

### `src/instrument_harness_lab/calibration.py`

教學重點：

- 純演算法模組。
- 不做 I/O。
- 適合 unit test。

### `src/instrument_harness_lab/controller.py`

教學重點：

- 串接儀器與校正。
- 把 workflow 放在一個清楚位置。

### `src/instrument_harness_lab/cli.py`

教學重點：

- CLI 是邊界。
- `print` 只出現在 CLI 或 sensor runner。

### `src/instrument_harness_lab/sensors/architecture_sensor.py`

教學重點：

- 架構規則可以被程式檢查。
- 用 AST 檢查 import 方向。

### `src/instrument_harness_lab/sensors/maintainability_sensor.py`

教學重點：

- 可維護性可以先用簡單規則感測。
- 不需要一開始就做很複雜的工具。

### `src/instrument_harness_lab/sensors/run_feedback.py`

教學重點：

- 給 agent 與工程師一個單一入口。
- 讓「該跑哪些檢查」不要靠記憶。

### `tests/test_calibration_behaviour.py`

教學重點：

- 測行為，而不是只測 implementation detail。
- stable/rejected case 都要有。

### `tests/test_sensors.py`

教學重點：

- sensor 本身也要測。
- harness 也是產品的一部分。

## 18. 三小時課程腳本

### 0:00-0:15 開場

講師說：

> 今天不是要教大家相信 coding agent，而是教大家怎麼約束 coding agent。工程管理裡最危險的是把不可控的東西放進交付流程，所以我們要建立 harness。

活動：

- 問學員用 agent 最擔心什麼。
- 把答案分類成規格、架構、測試、維護、語意。

### 0:15-0:40 原文概念解釋

照這個順序講：

1. Harness。
2. Guides 與 feedforward。
3. Sensors 與 feedback。
4. Computational 與 inferential。
5. Steering loop。
6. Keep quality left。

不要一開始講所有名詞，先用流程圖。

### 0:40-1:00 專案導覽

跑：

```bash
uv sync --dev
uv run instrument-lab calibrate --fixture stable
uv run instrument-lab calibrate --fixture drifted
```

講解：

- `stable` 是正常儀器。
- `drifted` 是非線性漂移儀器。
- CLI 輸出的是校正憑證。

### 1:00-1:25 Harness baseline

跑：

```bash
uv run ruff check .
uv run pytest --cov=instrument_harness_lab --cov-report=term-missing
uv run harness-sensors --with-tests
```

講解每個指令屬於哪個 harness。

### 1:25-1:35 休息

### 1:35-2:05 練習一：新增 fixture

任務：

> 新增一個 `noisy` fixture，讓校正因最大誤差過高而失敗。

學員要改：

- `instrument.py`
- `tests/test_calibration_behaviour.py`

驗收：

```bash
uv run instrument-lab calibrate --fixture noisy
uv run harness-sensors --with-tests
```

討論：

- 這是 behaviour harness 還是 architecture harness？
- 需要更新 guide 嗎？

### 2:05-2:30 練習二：故意破壞架構

任務：

> 故意讓 `calibration.py` import `cli.py`，觀察 sensor。

跑：

```bash
uv run harness-sensors
```

討論：

- sensor message 是否足夠清楚？
- 如果 agent 看到這個 message，能否修正？

### 2:30-2:50 練習三：Steering loop

任務：

> 每組選一個剛剛出現或想像中的錯誤，新增 guide 或 sensor。

範例題：

- 禁止 fixture 使用未固定 seed 的亂數。
- 禁止 calibration module 讀取環境變數。
- 要求所有 CLI JSON 都包含 `accepted`。
- 要求 spec 中的驗收門檻與程式常數一致。

### 2:50-3:00 收斂

講師總結：

> Harness Engineering 的成熟度，不是看你有多少工具，而是看你能不能把反覆出現的錯誤轉成前置 guide 或後置 sensor。

## 19. 講師示範用指令清單

### 安裝與同步

```bash
uv sync --dev
```

### 正常校正

```bash
uv run instrument-lab calibrate --fixture stable
```

預期：

- `accepted: true`
- `r_squared` 接近 1
- `max_absolute_error` 小於 1.5

### 漂移校正

```bash
uv run instrument-lab calibrate --fixture drifted
```

預期：

- `accepted: false`
- `max_absolute_error` 大於 1.5
- `r_squared` 明顯下降

### 跑完整 feedback sensors

```bash
uv run harness-sensors --with-tests
```

預期：

```text
[sensor-pass] architecture, maintainability, and requested tests passed
```

### 跑 coverage

```bash
uv run pytest --cov=instrument_harness_lab --cov-report=term-missing
```

預期：

- 測試通過。
- coverage 高於 90%。

## 20. 學員常見問題與講師回答

### 問：這不就是測試嗎？

答：

> 測試是 harness 的一部分，但 harness 不只是測試。Harness 還包含修改前的 guides、架構規則、語意 review、工具入口、以及人類根據錯誤更新控制系統的 steering loop。

### 問：有了 AI reviewer，還需要 deterministic sensor 嗎？

答：

> 需要。能用 deterministic sensor 抓的問題，應該優先用 deterministic sensor。AI reviewer 適合補語意判斷，不適合取代快速、穩定、便宜的 feedback。

### 問：為什麼不直接接真實儀器做 end-to-end？

答：

> 真實儀器測試很重要，但它太慢、太貴、太不穩定，不適合做最左側 feedback。這個專案先用 deterministic simulator，把大部分邏輯錯誤提早抓出來。

### 問：這些 sensor 會不會太簡單？

答：

> 教學用 sensor 故意保持簡單，重點是讓學員理解模式。真實專案可以逐步加入更完整的 static analysis、contract tests、hardware-in-the-loop tests 與 CI。

### 問：agent 還是可能通過所有 sensor 但寫錯嗎？

答：

> 會。Harness 不是保證正確，它只保證你設計過的控制會被執行。這就是為什麼 human steering loop 很重要：每次漏抓問題，都要問是否要新增 guide 或 sensor。

## 21. 講師檢核表

上課前確認：

- `uv sync --dev` 成功。
- `uv run harness-sensors --with-tests` 通過。
- GitHub repo 可以開啟。
- 投影片或白板上有 feedforward/feedback 圖。
- 能清楚說明 stable 與 drifted fixture 的差異。

上課中確認：

- 學員能分辨 guide 與 sensor。
- 學員能分辨 computational 與 inferential。
- 學員能把錯誤分類到 maintainability、architecture 或 behaviour。
- 學員能提出至少一個新增 guide 或 sensor。

上課後作業：

- 請學員回到自己的專案，列出 5 個常見 agent failure modes。
- 每個 failure mode 至少提出一個 guide 或 sensor。
- 挑一個最便宜的 computational sensor 先實作。

## 22. 如何把這份教材改成你自己的儀器課程？

如果你的客戶不是光譜儀，而是其他儀器，可以這樣替換：

| 本教材 | 可替換成 |
| --- | --- |
| 光譜儀濃度校正 | 溫控箱 PID 校正、泵浦流量校正、DAQ 訊號校正 |
| `stable` fixture | 正常硬體 profile |
| `drifted` fixture | 老化、偏移、噪聲、非線性、通訊失敗 |
| R² 與最大誤差 | 溫度 overshoot、settling time、流量偏差、訊號雜訊 |
| architecture sensor | 依照該系統模組邊界重寫 |
| product spec | 改成該儀器的驗收規格 |

## 23. 最後總結

你可以用下面這段話收尾：

> Harness Engineering 是把工程團隊的知識變成控制系統。Guides 在修改前引導方向，sensors 在修改後提供回饋，computational controls 負責快速且穩定的檢查，inferential controls 補足語意判斷，人類則負責 steering loop。對儀器軟體團隊來說，這代表我們可以把校正規格、硬體風險、架構邊界與測試習慣，變成 coding agent 可以遵守、可以被檢查、可以持續改進的工程系統。

## 24. 原文 Sidebars 與補充觀念

原文除了主線章節，也有幾個 sidebar。這些內容很適合在學員問比較深入問題時補充。

### 24.1 Metaphors only go so far

原文用 harness、feedforward、feedback、sensor、governor 這些控制系統隱喻來幫助理解，但講師要提醒學員：

> 隱喻是用來幫助思考，不是嚴格的工程等價。

不要把 coding agent 完全當成可精準建模的機械系統。LLM 有非 deterministic 特性，也可能誤解需求。Harness Engineering 的價值是提高信心與降低監督成本，不是把 AI 變成完全可證明正確的系統。

本專案示範方式：

- `harness-sensors` 通過，只代表目前 sensors 沒有抓到問題。
- 它不代表校正方法絕對適合所有儀器。
- 所以還需要 `guides/inferential-review.md` 與人類 review。

講師可用問題：

> 如果所有測試都通過，但客戶說校正模型不符合新機種，這是測試失敗、guide 失敗，還是 human steering 的問題？

建議答案：

- 這代表 behaviour guide 沒有描述新機種需求。
- 可能也代表 fixture 不足。
- 要更新 product spec、fixture 與 tests。

### 24.2 Harness Engineering 與 Context Engineering 的關係

原文指出，context engineering 提供讓 guides 與 sensors 被 agent 使用的方法；user harness 則是 context engineering 的一種具體形式。

用白話講：

- Context engineering 問的是：agent 執行任務時看得到哪些上下文？
- Harness engineering 問的是：哪些上下文與檢查能讓 agent 被有效控制？

本專案對應：

| Context | Harness 角色 |
| --- | --- |
| `AGENTS.md` | agent 工作規則 |
| `guides/product-spec.md` | 功能規格 feedforward |
| `guides/architecture.md` | 架構 feedforward |
| `tests/` | 行為 feedback |
| `sensors/` | 自訂 feedback |

講師講法：

> Context engineering 是把資料放到 agent 眼前；Harness engineering 是決定哪些資料、工具、測試與回饋能形成控制系統。

### 24.3 Ambient Affordances

Ambient affordances 可以理解成「環境中自然存在、讓 agent 更容易做對的線索與工具」。

在傳統開發中，人類會自然看懂很多環境線索：

- 專案資料夾結構。
- 測試命名方式。
- README 指令。
- CI 狀態。
- IDE 警告。
- 型別提示。

coding agent 不一定會自然理解這些線索，所以我們要把它們設計得更明確。

本專案如何提供 ambient affordances：

- `src/instrument_harness_lab/` 清楚分層。
- `tests/test_calibration_behaviour.py` 用 behaviour 命名。
- `harness-sensors` 是單一品質入口。
- `README.md` 第一頁就列出要跑的指令。
- `guides/` 資料夾讓 agent 知道規格在哪裡。

講師示範：

> 你可以請學員看 repo 30 秒，問他們不用讀完整文件，能不能猜出這個專案怎麼跑、怎麼測、規格在哪裡。這就是 ambient affordances 的效果。

### 24.4 Ashby's Law

原文提到 Ashby's Law：控制器需要有足夠 variety 才能治理被控制系統。

在 coding agent 情境：

- agent 能產生的東西很多。
- 專案越大、越混亂、越沒有固定 topology，agent 可能走偏的方向越多。
- harness 如果太弱，就管不住這些變化。

本專案的策略是先降低 variety：

- 單一儀器情境。
- 單一校正流程。
- 明確模組邊界。
- deterministic fixture。
- 有限但清楚的 sensors。

講師講法：

> 不要第一天就想替整個大型 legacy 系統建立完整 harness。先選一條高價值、邊界清楚的流程，讓 harness 有能力管住它。

## 25. Change Lifecycle：把 feedforward 與 feedback 放在不同時間點

原文強調，feedback sensors 要根據成本、速度與重要性分配到不同時間點。本專案可以用下表講解。

| 時間點 | 本專案範例 | 類型 | 說明 |
| --- | --- | --- | --- |
| 修改前 | `AGENTS.md` | feedforward | 先告訴 agent 工作規則 |
| 修改前 | `guides/product-spec.md` | feedforward | 先告訴 agent 行為規格 |
| 修改前 | `guides/architecture.md` | feedforward | 先告訴 agent 架構邊界 |
| 修改後、commit 前 | `uv run ruff check .` | feedback | 快速維護性檢查 |
| 修改後、commit 前 | `uv run pytest` | feedback | 快速行為檢查 |
| 修改後、commit 前 | `uv run harness-sensors` | feedback | 自訂架構與維護性檢查 |
| PR review 前 | `guides/inferential-review.md` | inferential feedback | 語意檢查 |
| CI | 重跑所有快速 sensors | feedback | 避免本機漏跑 |
| 夜間或週期性 | coverage quality、dead code、dependency scan | continuous drift sensor | 監控逐漸累積的問題 |
| 執行環境 | latency、error rate、log anomaly | runtime feedback | 對已部署系統觀測 |

### 講師要強調

不是每個 sensor 都要每次跑。

- 快的 computational sensor：commit 前跑。
- 較慢的 inferential sensor：PR 或重要變更跑。
- 更貴的 mutation testing 或硬體測試：CI 或夜間跑。
- runtime feedback：部署後持續觀測。

## 26. Continuous Drift 與 Health Sensors

### 原文概念

有些問題不是單次 change 造成，而是慢慢累積：

- dead code 變多。
- 測試品質下降。
- 相依套件老化。
- 架構邊界逐漸模糊。
- runtime latency 逐漸變差。
- log 品質不足，導致故障時查不出原因。

這些問題需要 continuous sensors，不一定跟某一次 commit 綁在一起。

### 儀器公司可用例子

| Drift 類型 | Sensor 例子 |
| --- | --- |
| fixture 老化 | 定期比較 fixture 與真實硬體 sample |
| 校正規格漂移 | 檢查 spec、程式常數、測試門檻是否一致 |
| 測試品質下降 | mutation testing 或 coverage quality |
| 相依套件風險 | dependency scanner |
| 架構腐敗 | 定期 architecture sensor 報表 |
| 現場儀器異常 | runtime log anomaly detection |

### 本專案目前做到哪裡？

目前本專案做到 commit 前 feedback：

```bash
uv run harness-sensors --with-tests
```

尚未實作 continuous drift sensors，因為教學第一階段要先讓學員理解最小可行 harness。

課堂延伸題：

> 請設計一個 sensor，檢查 `guides/product-spec.md` 裡的 R² 門檻是否和 `calibration.py` 的 `MIN_R_SQUARED` 一致。

這題可以引出：

- 文件與程式同步問題。
- harness coherence 問題。
- sensor coverage 問題。

## 27. Approved Fixtures 與 Behaviour Harness 的限制

### 原文概念

原文在 behaviour harness 中提到 approved fixtures pattern。重點是：不要只相信 agent 自己產生的測試，要有被人類認可、代表真實需求的 fixture 或 golden examples。

### 本專案對應

```text
stable fixture
drifted fixture
tests/test_calibration_behaviour.py
```

`stable` 與 `drifted` 不是隨便產生的資料，而是課堂中用來代表兩種儀器狀態：

- `stable`：正常線性量測，應該通過。
- `drifted`：非線性漂移，應該失敗。

### 講師要提醒

Approved fixture 的品質很重要。如果 fixture 本身不代表真實世界，測試通過也沒意義。

可問學員：

> 誰有資格 approve fixture？軟體工程師、儀器工程師、品保、還是客戶？

建議答案：

- 軟體工程師可以建立 fixture。
- 儀器工程師或領域專家應確認 fixture 是否合理。
- 品保可以確認 fixture 是否對應驗收流程。

## 28. 原文的 Open Questions：這些問題可以當結尾討論題

原文最後提醒，Harness Engineering 還有很多未解問題。這些很適合變成課堂結尾討論。

### 28.1 Guides 與 sensors 長大後如何保持一致？

本專案例子：

- `guides/product-spec.md` 寫 `r_squared >= 0.995`。
- `calibration.py` 也有 `MIN_R_SQUARED = 0.995`。
- 如果其中一邊改了，另一邊沒改，harness 就不一致。

討論：

- 是否要新增文件一致性 sensor？
- 規格是否應改成 machine-readable，例如 YAML？
- 文件與程式誰是 single source of truth？

### 28.2 當指令與 feedback 衝突時，agent 該相信誰？

例子：

- guide 說函式要短。
- 一個緊急修復需求要求快速 patch。
- sensor 說函式太長。

討論：

- agent 不應自行做高風險取捨。
- 人類要定義優先序。
- 可以在 guide 中寫清楚例外流程。

### 28.3 Sensor 從來沒失敗，是品質很好還是 sensor 太弱？

這是非常重要的問題。

如果 sensor 永遠不失敗，可能有兩種原因：

- 團隊真的做得很好。
- sensor 沒有檢查到真正風險。

講師活動：

> 請學員故意製造一個他們擔心的錯誤，看現有 harness 抓不抓得到。

抓不到時，不是責怪 sensor，而是進入 steering loop。

### 28.4 Harness coverage 如何衡量？

測試有 coverage，但 harness 也需要 coverage 思維。

可問：

- 我們列出的 agent failure modes，有多少被 guide 覆蓋？
- 有多少被 sensor 覆蓋？
- 哪些只能靠人類 review？
- 哪些值得投資成 computational sensor？

本專案可做練習：

| Failure mode | Guide | Sensor | 是否已覆蓋 |
| --- | --- | --- | --- |
| 忘記 accepted 欄位 | product spec | behaviour test | 已覆蓋 |
| 演算法直接 print | AGENTS.md | maintainability sensor | 已覆蓋 |
| 模組反向依賴 | architecture guide | architecture sensor | 已覆蓋 |
| fixture 不合理 | product spec | 人類 review | 部分覆蓋 |
| spec 與程式常數不一致 | product spec | 尚未實作 | 未覆蓋 |

## 29. 原文目錄覆蓋檢查表

講師備課時，可以用這張表確認每個原文段落都有講到。

| 原文段落 | 本手冊位置 | 本專案示範 |
| --- | --- | --- |
| Feedforward and Feedback | 第 4、5、6、7 章 | `AGENTS.md`、`guides/`、`harness-sensors` |
| Computational vs Inferential | 第 8、9 章 | AST sensors、pytest、`inferential-review.md` |
| The steering loop | 第 10 章 | 練習三：新增 guide 或 sensor |
| Timing: Keep quality left | 第 11、25 章 | `uv run harness-sensors --with-tests` |
| Continuous drift and health sensors | 第 26 章 | 延伸題 |
| Regulation categories | 第 12 章 | maintainability、architecture、behaviour |
| Maintainability harness | 第 12.1 章 | `maintainability_sensor.py`、ruff、coverage |
| Architecture fitness harness | 第 12.2 章 | `architecture_sensor.py` |
| Behaviour harness | 第 12.3、27 章 | approved fixtures、behaviour tests |
| Harnessability | 第 13 章 | 純函式、deterministic fixture、分層 |
| Harness templates | 第 14 章 | repo 結構作為儀器專案樣板 |
| The role of the human | 第 16 章 | human steering loop |
| A starting point and open questions | 第 28 章 | harness coherence、coverage、衝突處理 |
| Metaphors only go so far | 第 24.1 章 | sensor-pass 不等於絕對正確 |
| Context engineering | 第 24.2 章 | guides/sensors 作為 agent context |
| Ambient affordances | 第 24.3 章 | repo 結構與單一指令入口 |
| Ashby's Law | 第 15、24.4 章 | 降低專案 variety |
