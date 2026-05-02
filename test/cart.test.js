import assert from "node:assert/strict";
import test from "node:test";

import {
  FREE_SHIPPING_THRESHOLD,
  addItem,
  createCart,
  discount,
  formatTwd,
  shipping,
  subtotal,
  totals,
} from "../src/cart.js";

test("購物車可以加入商品並計算小計", () => {
  let cart = createCart();
  cart = addItem(cart, "bag");
  cart = addItem(cart, "cup");

  assert.equal(subtotal(cart), 1200);
});

test("HARNESS10 折扣碼提供 10% 折扣", () => {
  let cart = createCart();
  cart = addItem(cart, "bag");
  cart = addItem(cart, "cup");

  assert.equal(discount(cart, "HARNESS10"), 120);
});

test("折扣碼大小寫與前後空白不影響判斷", () => {
  let cart = createCart();
  cart = addItem(cart, "lamp");

  assert.equal(discount(cart, " harness10 "), 65);
});

test("滿 NT$1,000 免運，未滿收 NT$80", () => {
  let cart = createCart();
  cart = addItem(cart, "bag");
  assert.equal(shipping(cart), 80);

  cart = addItem(cart, "cup");
  assert.equal(subtotal(cart) >= FREE_SHIPPING_THRESHOLD, true);
  assert.equal(shipping(cart), 0);
});

test("總金額等於小計減折扣加運費", () => {
  let cart = createCart();
  cart = addItem(cart, "bag");
  cart = addItem(cart, "cup");

  assert.deepEqual(totals(cart, "HARNESS10"), {
    subtotal: 1200,
    discount: 120,
    shipping: 0,
    total: 1080,
  });
});

test("未知商品會回報清楚錯誤", () => {
  assert.throws(() => addItem(createCart(), "missing"), /unknown product/);
});

test("金額顯示使用台幣格式", () => {
  assert.equal(formatTwd(1200), "NT$1,200");
});
