# Behaviour Guide：光譜儀校正規格

這份文件是 behaviour harness 的 feedforward guide。

## 使用者故事

身為儀器公司軟體工程師，我要在光譜儀交機前執行濃度標準品校正，讓系統可以判斷儀器本次校正是否通過，並輸出可追溯的校正憑證。

## 功能規格

- 系統輸入一組標準濃度與對應儀器讀值。
- 系統用一次線性迴歸建立校正曲線。
- 系統輸出：
  - `slope`
  - `intercept`
  - `r_squared`
  - `max_absolute_error`
  - `accepted`
  - 每個標準點的原始讀值與預測誤差
- 驗收條件：
  - `r_squared >= 0.995`
  - `max_absolute_error <= 1.5`

## 課堂變更題

1. 加入新的儀器 fixture，讓校正失敗但錯誤訊息清楚。
2. 修改驗收規格，觀察 tests 與 sensors 如何回饋。
3. 故意讓 CLI 直接計算校正，觀察 architecture sensor 如何阻擋。
