import * as global from './globals.js'

//
const login = new global.Login();
const logs = new global.MessageLogs();

//
login.init_elements();

login.BUTT_CAPTCHA_GET.addEventListener('click', (e) => {
    e.preventDefault();

    //
    fetch('/captcha/generate')
    .then(response => response.blob())
    .then(blob => {
        const img_url = URL.createObjectURL(blob);
        // console.log(img_url);
        // console.log(login.IMG_CAPTCHA);

        login.IMG_CAPTCHA.set("src", img_url);
    });
})

login.BUTT_FORM_FINISH.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const form_credentials = login.FORM_CREDENTIALS.get();
    const form_captcha = login.FORM_CAPTCHA.get();

    const formData = global.forms_validation(form_credentials, form_captcha);
    if(!formData)
        return;

    //
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
            window.localtion = href_link;
            return;
        }

        logs.CLEAN();
        logs.ADD(message["type"], message["content"]);
    });
})
