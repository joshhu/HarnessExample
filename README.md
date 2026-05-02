# Instrument Harness Lab

這是一個給儀器公司軟體工程師使用的 Harness Engineering 教學專案。案例取材自
Birgitta Böckeler 在 Martin Fowler 網站發表的
[Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
，並把文章中的觀念落成可以執行、可以測試、可以延伸的儀器校正服務範例。

本專案假設團隊正在維護一套「光譜儀濃度校正」軟體。工程師或 coding agent 每次修改校正演算法、儀器模擬器、CLI 或測試時，都要被一組 feedforward guides 與 feedback sensors 約束，讓品質問題盡量在 commit 前被發現。

## 核心學習目標

- 用 guides 在 agent 或工程師動手前提供 feedforward 控制。
- 用 sensors 在修改後提供 feedback，讓問題可以自我修正。
- 同時示範 computational controls 與 inferential controls。
- 示範 maintainability harness、architecture fitness harness、behaviour harness。
- 把品質檢查往左移，讓儀器軟體的錯誤在更早的階段出現。
- 練習 human steering loop：從重複出現的錯誤反推新的 guide 或 sensor。

## 快速開始

```bash
uv sync --dev
uv run instrument-lab calibrate --fixture stable
uv run harness-sensors --with-tests
uv run pytest --cov=instrument_harness_lab --cov-report=term-missing
```

也可以先讀設計文件：

```bash
open docs/TEACHING_MANUAL.md
open docs/HARNESS_ENGINEERING_DESIGN.md
open docs/LESSON_PLAN.md
```

## 專案結構

```text
.
├── AGENTS.md                         # feedforward guide：給 coding agent 的專案規則
├── docs/
│   ├── TEACHING_MANUAL.md            # 講師用完整教學手冊
│   ├── HARNESS_ENGINEERING_DESIGN.md # 原文觀念到本專案元件的完整對應
│   └── LESSON_PLAN.md                # 課程流程與實作練習
├── guides/                           # feedforward guides
├── src/instrument_harness_lab/        # 可執行的儀器校正服務
├── tests/                            # behaviour 與 sensor 測試
└── pyproject.toml
```

## 可執行功能

`instrument-lab calibrate` 會產生一份校正憑證 JSON，內容包含線性校正係數、R²、最大誤差與是否通過驗收。預設 fixture 是 deterministic 的，因此適合課堂中做重複測試。

```bash
uv run instrument-lab calibrate --fixture stable
```

`harness-sensors` 會執行 computational feedback sensors：

```bash
uv run harness-sensors
uv run harness-sensors --with-tests
```

## 文件來源

- Martin Fowler 網站原文：Harness Engineering 文章，2026-04-02 發布。
- pytest 官方文件：`pyproject.toml` 可透過 `[tool.pytest.ini_options]` 設定測試。
- uv 官方文件：`uv run` 會在執行命令前同步專案環境，`uv sync --dev` 會安裝開發相依套件。
