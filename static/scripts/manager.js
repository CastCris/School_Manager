import * as global from './globals.js'

//
const manager = new global.Manager();
manager.init_elements();

manager.SLCT_ENTITY_NAME.addEventListener('change', (e) => {
    e.preventDefault();

    //
    const value = e.target.value;
    const json = { "entity_name": value };

    fetch('/auth/manager/select/entity', {
        method: 'POST',
        headers: {'Content-Type': "application/json; charset=utf-8"},

        body: JSON.stringify(json)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
});

manager.BUTT_FORM_CRUD_SUBMIT.addEventListener('click', (e) => {
    e.preventDefault();

    //
    console.log('submited forms!');
});
