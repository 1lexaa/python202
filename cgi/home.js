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