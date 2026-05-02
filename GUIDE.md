# Harness Shop Guide

這份檔案是本專案的 **feedforward guide**。  
在修改程式前，先看這裡；它的目的不是解釋所有程式，而是讓工程師或 coding agent 一開始就不要走錯方向。

## 產品規格

這是一個小型電商網站，使用者可以：

- 看見 3 個商品。
- 把商品加入購物車。
- 使用折扣碼 `HARNESS10` 取得 10% 折扣。
- 未滿 NT$1,000 運費 NT$80，滿 NT$1,000 免運。
- 清楚看到小計、折扣、運費、總金額。

## 架構規則

- `src/cart.js` 只放購物車商業邏輯，不可以操作 DOM。
- `src/app.js` 只負責把畫面和 `cart.js` 接起來。
- `index.html` 只放頁面結構，不放商業計算。
- `test/cart.test.js` 是 feedback sensor，規格改了就要同步更新測試。
- `harness/check.js` 是額外 sensor，用來檢查專案邊界。

## 講師故意破壞示範

上課時可以故意做這些事，讓學員看到 feedback：

- 把 `src/cart.js` 的免運門檻改錯。
- 在 `src/cart.js` 使用 `document.querySelector`。
- 從 `index.html` 移除 `type="module"`。
- 從 README 移除某個 Harness Engineering 觀念。
