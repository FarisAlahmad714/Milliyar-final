var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    var productName = this.dataset.name;
    var price = this.dataset.price;
    var stock = this.dataset.stock;
    console.log(
      "productId :",
      productId,
      "action:",
      action,
      "name",
      productName,
      "stock",
      stock,
      "price",
      price
    );
    console.log("hello");
    console.log("USER:", user);

    // if (user == "AnonymousUser") {
    addCookieItem(productId, action, productName, price, stock);
    // } else {
    // updateUserOrder(productId, action, productName, stock);
    // }
  });
}

function addCookieItem(productId, action, productName, price, stock) {
  console.log("Not Logged In");
  if (action == "add") {
    if (cart[productId] == undefined) {
      alert("Product is Successfully add1" + productName);
      cart[productId] = { quantity: 1 };
    } else {
      if (stock <= cart[productId].quantity) {
        alert(`sorry we not much stock. you cant add more item`);
      } else {
        cart[productId]["quantity"] += 1;
        alert("Product is Successfully add1" + productName);
      }
    }
  }
  if (action == "remove") {
    try {
      if (cart[productId]) {
        cart[productId]["quantity"] -= 1;

        let totalCart = 0;

        for (const property in cart) {
          totalCart += cart[property]["quantity"];
        }
        document.getElementById("totalCartItems").innerHTML = totalCart;

        // }
        //  else {
        // let cartitem = 0;
        // cartitem += cart[productId]["quantity"];
        document.getElementById(`cq${productId}`).innerHTML =
          cart[productId]["quantity"];
        // document.getElementById("totalCartItems").innerHTML = cartitem;

        let currentPrice = document
          .getElementById(`gettotal${productId}`)
          .innerText.slice(1);

        document.getElementById(`gettotal${productId}`).innerHTML = `$  ${
          Number(currentPrice) - Number(price)
        }.00`;

        let totalCartPrice = document
          .getElementById(`totalCartPrice`)
          .innerText.slice(1);
        // console.log(totalCartPrice);
        document.getElementById("totalCartPrice").innerHTML = `$${
          Number(totalCartPrice) - Number(price)
        }.00`;
        // location.reload();

        if (cart[productId]["quantity"] <= 0) {
          delete cart[productId];
          location.reload();
        }
      }
    } catch {}

    // alert("Product is Successfully remove" + productName);
    // try {
    //   cart[productId]["quantity"] -= 1;
    // } catch {
    //   console.log("Cart is already empty");
    // }
    // try {
    // if (cart[productId]["quantity"] <= 0) {
    //   console.log;
    //   ("Remove Item ");
    //   delete cart[productId];
    //   document.getElementById(`cq${productId}`).innerHTML = 0;
    //   document.getElementById(`gettotal${productId}`).innerHTML = `$ 0.00`;

    //   let totalCartPrice = document
    //     .getElementById(`totalCartPrice`)
    //     .innerText.slice(1);
    //   document.getElementById("totalCartPrice").innerHTML = `$${
    //     Number(totalCartPrice) - Number(price)
    //   }.00`;

    // }
    // } catch {
    //   console.log("item removed");
    // }
  }

  if (action == "addcart") {
    // alert("Product is Successfully add" + productName);

    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      console.log(stock, "stk", cart[productId].quantity);
      if (Number(stock) <= cart[productId].quantity) {
        alert(`sorry we not much stock. you cant add more item`);
      } else {
        cart[productId]["quantity"] += 1;
        let cartitem = 0;
        cartitem += cart[productId]["quantity"];
        document.getElementById(`cq${productId}`).innerHTML = cartitem;
        let currentPrice = document
          .getElementById(`gettotal${productId}`)
          .innerText.slice(1);

        document.getElementById(`gettotal${productId}`).innerHTML = `$  ${
          Number(currentPrice) + Number(price)
        }.00`;

        let totalCartPrice = document
          .getElementById(`totalCartPrice`)
          .innerText.slice(1);
        // console.log(totalCartPrice);
        document.getElementById("totalCartPrice").innerHTML = `$${
          Number(totalCartPrice) + Number(price)
        }.00`;

        let totalCart = 0;
        for (const property in cart) {
          totalCart += cart[property]["quantity"];
        }
        document.getElementById("totalCartItems").innerHTML = totalCart;
      }
    }
  }
  let totalCart = 0;
  for (const property in cart) {
    totalCart += cart[property]["quantity"];
  }
  document.getElementById("cart-total1").innerHTML = totalCart;
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";

  // location.reload();
}

function updateUserOrder(productId, action, productName, stock) {
  console.log("User is logged in ,sending data..");
  console.log(stock);
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      action: action,
      stock: stock,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // console.log("data:", data);
      if (action == "add" || action == "addcart") {
        if (stock <= data.quantity) {
          alert(`sorry we not much stock. you cant add more item`);
        } else {
          if (action == "add") {
            alert("product is successfuly added" + productName);
          }
        }
      }

      location.reload();
    });
}
