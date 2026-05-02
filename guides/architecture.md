# Architecture Fitness Guide

這份文件是 architecture fitness harness 的 feedforward guide。

## 模組邊界

```text
domain      <- calibration
domain      <- instrument
domain      <- controller
instrument  <- controller
calibration <- controller
controller  <- cli
```

允許的方向是由外層依賴內層；內層不得反向依賴外層。

## Fitness Functions

- `architecture_sensor` 會解析 AST import，檢查模組依賴方向。
- `maintainability_sensor` 會檢查函式長度、分支複雜度、CLI 輸出邊界。
- pytest behaviour tests 會確認校正結果符合規格。

## 設計理由

儀器軟體常見風險不是演算法本身而已，而是 I/O、儀器狀態、校正規格、使用者介面混在一起後難以測試。本範例刻意把校正演算法做成純函式，讓 computational sensors 可以快速、穩定地回饋。
