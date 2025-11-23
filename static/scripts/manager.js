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
        const message = data["message"];
        const entity_fields = data["entity_fields"];

        console.log(entity_fields, data);
        if(entity_fields != undefined){
            manager.ENTITY_FIELD = entity_fields;
            manager.build_entity_field();

            return;
        }

        logs.CLEAN();
        logs.ADD(message["type"], message["content"]);
    });
});

manager.SLCT_CRUD_OPERATION.addEventListener('change', (e) => {
    e.preventDefault();

    //
    const value = e.target.value;

    console.log(value);
});

manager.BUTT_FORM_CRUD_SUBMIT.addEventListener('click', (e) => {
    e.preventDefault();

    //
    console.log('submited forms!');
});
