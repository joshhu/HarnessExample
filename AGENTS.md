# Instrument Harness Lab Agent Guide

本檔案是本專案的 feedforward guide。工程師或 coding agent 修改程式前，必須先理解這些規則。

## 語言與環境

- 對話、註解與文件使用繁體中文台灣用語。
- Python 環境只使用 `uv`，不得使用原生 `pip install`。
- 儀器模擬必須 deterministic，測試不可依賴不可重現的亂數。

## 架構規則

- `domain.py` 只能放資料模型與純商業語意，不得依賴其他專案模組。
- `instrument.py` 只能處理儀器資料取得與模擬，不得知道 CLI 或 sensor。
- `calibration.py` 只能處理校正演算法與驗收規則，不得做 I/O。
- `controller.py` 負責串接儀器與校正流程。
- `cli.py` 是唯一可以直接 `print` 使用者輸出的模組。
- `sensors/` 只能讀程式碼與執行檢查，不得修改產品程式。

## 品質門檻

- 每個新功能都要有測試。
- 變更後至少執行 `uv run harness-sensors --with-tests`。
- 若同一類錯誤出現第二次，要新增或更新 guide 或 sensor。
- 不要用大型框架包住這個教學範例；可讀性優先。

## 儀器領域規則

- 校正結果必須輸出 `accepted`，不能只輸出係數。
- 驗收條件要能被測試讀取，不得藏在 CLI 字串。
- 測試資料要保留原始濃度、量測值與預測值，便於追查偏差。
