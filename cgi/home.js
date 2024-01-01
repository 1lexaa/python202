document.addEventListener("DOMContentLoaded", () => {
  const auth_button = document.getElementById("auth-button");

  if (auth_button) auth_button.addEventListener("click", authButtonClick);

  const info_button = document.getElementById("info-button");

  if (info_button) info_button.addEventListener("click", infoButtonClick);

  const product_button = document.getElementById("product-button");

  if (product_button)
    product_button.addEventListener("click", productButtonClick);
});

function productButtonClick() {
  const user_token = getToken();

  if (!user_token) {
    console.log("Authentication required.");
    return;
  }

  fetch("/product", {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${userToken}`,
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      name: document.getElementById("product-name").value,
      price: document.getElementById("product-price").value,
      image: document.getElementById("product-image").value,
    }),
  })
    .then((r) => r.json())
    .then(console.log);
}

function authButtonClick() {
  const user_login = document.getElementById("user-login");

  if (!user_login) throw "Element #user-login not found";

  const user_password = document.getElementById("user-password");

  if (!user_password) throw "Element #user-password not found";

  const credentials = btoa(`${user_login.value}:${user_password.value}`);

  fetch("/auth", {
    headers: { Authorization: `Basic ${credentials}` },
  })
    .then((response) => {
      if (response.ok) return response.text();
      else console.log("Authentication failed.");
    })
    .then((token) => {
      if (token) {
        saveToken(token);
        console.log("Authentication successful.");
      }
    });
}

function infoButtonClick() {
  const user_token = getToken();

  if (!user_token) {
    console.log("Authentication required.");
    return;
  }

  fetch(`/auth`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${user_token}`,
      "My-Header": "my-value",
    },
  })
    .then((r) => r.json())
    .then(console.log);
}

function saveToken(token) {
  localStorage.setItem("user-token", token);
}

function getToken() {
  return localStorage.getItem("user-token");
}
