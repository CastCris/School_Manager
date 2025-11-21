import * as global from './globals.js'

//
const login = new global.Login();

//
login.init_elements();

login.BUTT_CAPTCHA_GET.addEventListener('click', (e) => {
    e.preventDefault();

    fetch('/captcha/generate')
    .then(response => response.blob())
    .then(blob => {
        const img_url = URL.createObjectURL(blob);
        console.log(img_url);
        console.log(login.IMG_CAPTCHA);

        login.IMG_CAPTCHA.set("src", img_url);
    });
})
