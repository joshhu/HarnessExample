import { PRODUCTS, addItem, createCart, formatTwd, totals } from "./cart.js";

const productList = document.querySelector("#products");
const cartItems = document.querySelector("#cart-items");
const promoCode = document.querySelector("#promo-code");
const subtotalEl = document.querySelector("#subtotal");
const discountEl = document.querySelector("#discount");
const shippingEl = document.querySelector("#shipping");
const totalEl = document.querySelector("#total");

let cart = createCart();

function renderProducts() {
  productList.innerHTML = PRODUCTS.map(
    (product) => `
      <article class="product">
        <strong>${product.name}</strong>
        <span>${formatTwd(product.price)}</span>
        <button data-product-id="${product.id}" type="button">加入購物車</button>
      </article>
    `,
  ).join("");
}

function renderCart() {
  cartItems.innerHTML = cart.length
    ? cart
        .map((item) => `<li><span>${item.name}</span><strong>${formatTwd(item.price)}</strong></li>`)
        .join("")
    : `<li><span>尚未加入商品</span><strong>${formatTwd(0)}</strong></li>`;

  const summary = totals(cart, promoCode.value);
  subtotalEl.textContent = formatTwd(summary.subtotal);
  discountEl.textContent = `-${formatTwd(summary.discount)}`;
  shippingEl.textContent = formatTwd(summary.shipping);
  totalEl.textContent = formatTwd(summary.total);
}

productList.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-product-id]");
  if (!button) {
    return;
  }
  cart = addItem(cart, button.dataset.productId);
  renderCart();
});

promoCode.addEventListener("input", renderCart);

renderProducts();
renderCart();
