<<<<<<< HEAD
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
=======
document.addEventListener('DOMContentLoaded',() => {
    const authButton = document.getElementById('auth-button');
    if(authButton) authButton.addEventListener('click', authButtonClick );
    
    const infoButton = document.getElementById('info-button');
    if(infoButton) infoButton.addEventListener('click', infoButtonClick );
    
    const productButton = document.getElementById('product-button');
    if(productButton) productButton.addEventListener('click', productButtonClick );
});

function productButtonClick() {
    fetch("/product", {
        method: "PUT",
        body: JSON.stringify( {
            name:  document.getElementById("product-name" ).value,
            price: document.getElementById("product-price").value,
            image: document.getElementById("product-image").value
        } )
    }).then(r => r.json()).then(console.log);
}

function authButtonClick() {
    const userLogin = document.getElementById('user-login');
    if(!userLogin) throw "Element #user-login not found";
    const userPassword = document.getElementById('user-password');
    if(!userPassword) throw "Element #user-password not found";
    const credentials = btoa( `${userLogin.value}:${userPassword.value}` )
    // fetch(`/auth?login=${userLogin.value}&password=${userPassword.value}`)
    fetch('/auth',{
        headers: {
            'Authorization': `Basic ${credentials}`,
        }
    })
    .then(r => r.text()).then(console.log);
    // console.log("Clicked");
}
function infoButtonClick() {
    const userToken = document.getElementById('user-token');
    if(!userToken) throw "Element #user-token not found";

    fetch(`/auth`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${userToken.value}`,
            'My-Header': 'my-value'
        }
    })
    .then(r => r.json()).then(console.log);
    // console.log("Clicked");
}
/*
Д.З. Реалізувати прийом токена авторизації при автентифікації
користувача. У разі успішного прийому перенести одержане значення
у поле 'user-token', у разі відмови - стерти значення та видати
повідомлення про відхилення автентифікації.
*/
>>>>>>> 23607ae09fabcd30fcfc06703ad03519a3df1a4a
