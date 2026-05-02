export const PRODUCTS = [
  { id: "bag", name: "通勤背包", price: 780 },
  { id: "cup", name: "保溫杯", price: 420 },
  { id: "lamp", name: "閱讀燈", price: 650 },
];

export const FREE_SHIPPING_THRESHOLD = 1000;
export const SHIPPING_FEE = 80;
export const PROMO_CODE = "HARNESS10";
export const PROMO_RATE = 0.1;

export function createCart() {
  return [];
}

export function addItem(cart, productId) {
  const product = PRODUCTS.find((item) => item.id === productId);
  if (!product) {
    throw new Error(`unknown product: ${productId}`);
  }
  return [...cart, product];
}

export function subtotal(cart) {
  return cart.reduce((sum, item) => sum + item.price, 0);
}

export function discount(cart, promoCode) {
  if (promoCode.trim().toUpperCase() !== PROMO_CODE) {
    return 0;
  }
  return Math.round(subtotal(cart) * PROMO_RATE);
}

export function shipping(cart) {
  return subtotal(cart) >= FREE_SHIPPING_THRESHOLD ? 0 : SHIPPING_FEE;
}

export function totals(cart, promoCode = "") {
  const beforeDiscount = subtotal(cart);
  const promoDiscount = discount(cart, promoCode);
  const delivery = shipping(cart);
  return {
    subtotal: beforeDiscount,
    discount: promoDiscount,
    shipping: delivery,
    total: beforeDiscount - promoDiscount + delivery,
  };
}

export function formatTwd(amount) {
  return `NT$${amount.toLocaleString("zh-TW")}`;
}
