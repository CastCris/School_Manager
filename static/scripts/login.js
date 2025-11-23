import * as global from './globals.js'

//
const login = new global.Login();
const logs = new global.MessageLogs();

//
login.init_elements();

login.BUTT_CAPTCHA_GET.addEventListener('click', (e) => {
    e.preventDefault();

    //
    global.captchaIMG_generate(login.IMG_CAPTCHA.OBJECT);
})

login.BUTT_FORM_FINISH.addEventListener('click', async (e) => {
    e.preventDefault();

    //
    const form_credentials = login.FORM_CREDENTIALS.get();
    const form_captcha = login.FORM_CAPTCHA.get();

    const formData = global.forms_validation(form_credentials, form_captcha);
    if(!formData)
        return;

    const formData_json = Object.fromEntries(formData);

    fetch('/auth/login', {
        method: "POST",
        headers: {'Content-Type': "application/json; charset=utf-8"},

        body: JSON.stringify(formData_json)
    })
    .then(response => response.json())
    .then(data => {
        const message = data["message"];
        const href_link = data["href_link"];

        if(href_link != undefined){
            window.location.href = href_link;
            return;
        }

        logs.CLEAN();
        logs.ADD(message["type"], message["content"]);
    });
})

//
global.captchaIMG_generate(login.IMG_CAPTCHA.OBJECT);
