# Inferential Review Sensor Prompt

這份文件示範 inferential feedback sensor。它不在預設 CI 中自動呼叫 LLM，因為課堂環境不應要求 API key；但它提供給人工 review 或 AI review agent 使用。

## Review 任務

請以儀器軟體工程 reviewer 的角度檢查這次變更：

- 是否符合 `guides/product-spec.md` 的校正規格？
- 是否維持 `guides/architecture.md` 的模組邊界？
- 是否有把儀器領域語意藏在 CLI 或測試 fixture 裡？
- 是否有新增不可重現的亂數、時間相依或硬體相依行為？
- 是否有過度設計，導致教學範例不容易理解？
- 如果 computational sensor 沒有抓到問題，應新增哪一種 guide 或 sensor？

## 輸出格式

```text
Findings:
- [severity] 檔案:行號：問題與理由

Harness updates:
- 建議新增或修改的 guide/sensor
```
