# Harness Engineering 課程設計

## 對象

儀器公司軟體工程師，熟悉基本 Python 或其他後端語言，正在或即將使用 coding agent 協助開發。

## 時長

建議 3 小時工作坊。

## 課程流程

### 1. 觀念導入，30 分鐘

- Harness = model 外圍的控制系統。
- Feedforward guides：讓 agent 動手前更可能做對。
- Feedback sensors：讓 agent 動手後能自我修正。
- Computational controls：快、穩、可重複。
- Inferential controls：能做語意判斷，但較慢、較不穩定。

### 2. 跑 baseline，20 分鐘

```bash
uv sync --dev
uv run instrument-lab calibrate --fixture stable
uv run harness-sensors --with-tests
```

討論：

- 哪些檢查是 maintainability harness？
- 哪些檢查是 architecture fitness harness？
- 哪些檢查是 behaviour harness？

### 3. 實作練習一：新增失敗 fixture，35 分鐘

任務：新增一個 `noisy` fixture，讓校正因最大誤差過高而失敗。

驗收：

- CLI 可以執行 `uv run instrument-lab calibrate --fixture noisy`。
- 測試確認 `accepted` 為 `false`。
- sensor 全部通過。

### 4. 實作練習二：故意破壞架構，30 分鐘

任務：把 CLI 輸出邏輯放進 `calibration.py`，觀察 architecture 或 maintainability sensor 的回饋。

討論：

- sensor 訊號是否足夠讓 coding agent 自我修正？
- 錯誤訊息是否應更像「正向 prompt injection」？

### 5. 實作練習三：Steering Loop，40 分鐘

任務：學員從剛剛重複出現的錯誤中挑一個，新增 guide 或 sensor。

範例：

- 若多人忘記更新 behaviour spec，就新增文件一致性 sensor。
- 若多人把硬體 I/O 寫進演算法，就強化 architecture guide。
- 若多人讓測試 fixture 不可重現，就新增 random seed sensor。

### 6. 收斂與討論，25 分鐘

- 哪些檢查應該在 commit 前跑？
- 哪些檢查應該在 CI 或夜間 drift scan 跑？
- 哪些判斷仍然必須由資深工程師負責？

## 講師提示

- 不要把課程變成「工具列表」。重點是控制系統如何互相搭配。
- 每次 sensor 失敗，都要求學員判斷它屬於哪一種 feedback。
- 每次 guide 修改，都要求學員說明它預防哪一類 agent failure mode。
