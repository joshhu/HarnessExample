# Harness Engineering Design

本文說明如何把 Martin Fowler 網站文章中的 Harness Engineering 觀念，轉成一個儀器軟體工程師可以實作、測試與討論的專案。

## 案例背景

儀器公司正在開發一套光譜儀濃度校正服務。系統會讀取標準品濃度與儀器量測值，建立線性校正曲線，並判斷本次校正是否通過。課堂中的 coding agent 或工程師會被要求修改校正規格、加入儀器 fixture、擴充 CLI 或修正測試。

這個案例適合教 Harness Engineering，因為儀器軟體同時需要：

- 明確的功能行為：校正是否通過。
- 明確的架構邊界：演算法、儀器 I/O、CLI 不能混在一起。
- 快速 deterministic 測試：不依賴實體硬體也能回饋。
- 人類專業判斷：校正規格與風險取捨仍需要工程師決策。

## 原文觀念對應

| 原文觀念 | 本專案元件 | 用途 |
| --- | --- | --- |
| Harness | guides、sensors、tests、CLI、文件組成的外層控制系統 | 提高 agent 或工程師第一次做對的機率，並在錯誤送到人工 review 前自我修正 |
| Guides / feedforward | `AGENTS.md`、`guides/product-spec.md`、`guides/architecture.md` | 修改前先給規格、邊界與工作規則 |
| Sensors / feedback | `harness-sensors`、pytest、coverage、ruff | 修改後觀察結果並產生可修正訊號 |
| Computational controls | AST 架構檢查、maintainability scan、unit tests、coverage | 快速、可重複、適合每次修改都跑 |
| Inferential controls | `guides/inferential-review.md` | 用語意 review 補足 deterministic 工具不容易判斷的問題 |
| Steering loop | `docs/LESSON_PLAN.md` 的練習三 | 當錯誤重複發生，就更新 guide 或 sensor |
| Keep quality left | `uv run harness-sensors --with-tests` | 在 commit 或整合前先跑快速 sensors |
| Maintainability harness | `maintainability_sensor.py`、ruff、coverage | 控制複雜度、輸出邊界與可維護性 |
| Architecture fitness harness | `architecture_sensor.py`、`guides/architecture.md` | 控制模組依賴方向 |
| Behaviour harness | `tests/test_calibration_behaviour.py`、`guides/product-spec.md` | 驗證校正行為符合規格 |
| Harnessability | `domain/calibration/controller/cli` 分層、純函式演算法、deterministic fixture | 讓程式更容易被工具理解與檢查 |
| Harness templates | 本 repo 結構本身 | 可複製到其他儀器服務，如溫控箱、泵浦、資料擷取器 |
| Human role | 課程中的 review 與規格調整 | 人類決定規格、風險、例外與商業取捨 |
| Ashby 定律 | 限定專案 topology 為單一儀器校正服務 | 降低 agent 可能產出的變化範圍，讓 harness 足以治理 |

## Feedforward：Guides

### `AGENTS.md`

給 coding agent 或工程師的第一層規則，定義語言、工具、架構、測試與儀器領域約束。

### `guides/product-spec.md`

定義校正行為與驗收條件。這是 behaviour harness 的主要 feedforward。

### `guides/architecture.md`

定義模組依賴方向。這是 architecture fitness harness 的主要 feedforward。

### `guides/inferential-review.md`

提供 AI reviewer 或人工 reviewer 使用的語意檢查清單。它不是 deterministic sensor，但能檢查「看起來通過測試但方向錯了」的問題。

## Feedback：Sensors

### Architecture Sensor

`architecture_sensor.py` 解析 Python AST import，確認內層模組沒有依賴外層模組。這能防止 CLI 邏輯滲入校正演算法。

### Maintainability Sensor

`maintainability_sensor.py` 檢查：

- 函式是否過長。
- 分支複雜度是否過高。
- 是否在非 CLI 模組中直接 `print`。

### Behaviour Tests

pytest 測試儀器校正結果：

- 穩定 fixture 必須通過。
- 漂移 fixture 必須失敗。
- 每個標準點都要保留誤差資訊。

### Coverage

coverage 不是品質保證本身，但它能感測測試是否開始失去保護範圍。本專案設定 coverage 下限為 90%。

## 三種 Regulation Categories

### Maintainability Harness

目標是維持程式容易讀、容易改、容易測。工具包括 ruff、coverage、`maintainability_sensor.py`。

### Architecture Fitness Harness

目標是維持架構特性。這個範例的架構特性是「校正演算法純化」與「I/O 留在邊界」。工具包括 `guides/architecture.md` 與 `architecture_sensor.py`。

### Behaviour Harness

目標是確認功能真的符合儀器校正需求。工具包括 `guides/product-spec.md`、pytest、approved deterministic fixture 與人工 review。

## 課堂中的 Steering Loop

1. 學員先跑 `uv run harness-sensors --with-tests`，建立 baseline。
2. 講師指定一個變更，例如「把 R² 門檻改成 0.998」。
3. 學員修改程式與測試。
4. sensors 回饋錯誤。
5. 若錯誤代表規則缺失，學員新增 guide 或 sensor。
6. 討論這個新增的控制屬於 feedforward、feedback、computational 還是 inferential。

## 為什麼這是儀器公司的好案例

儀器軟體通常會面對硬體不穩定、校正規格嚴格、資料可追溯、維修成本高等問題。Harness Engineering 不是取代工程師，而是把工程師本來腦中的經驗外顯成 guides 與 sensors，讓 coding agent 或新進工程師不容易在相同地方重複犯錯。

## 已查證資料

- 原文於 2026-04-02 發布，重點包含 feedforward/feedback、computational/inferential、steering loop、keep quality left、regulation categories、harnessability、harness templates 與 human role。
- pytest 官方文件說明可在 `pyproject.toml` 中使用 `[tool.pytest.ini_options]` 設定測試參數。
- uv 官方文件說明 `uv run` 會在執行命令前同步專案環境，適合用於本專案的可重現開發流程。
