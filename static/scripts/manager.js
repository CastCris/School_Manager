import * as global from './globals.js'

//
const manager = new global.Manager();
manager.init_elements();

//
manager.SLCT_ENTITY_NAME.addEventListener('change', (e) => {
    e.preventDefault();

    //
    manager.entity_field_build();
});


manager.SLCT_CRUD_OPERATION.addEventListener('change', (e) => {
    e.preventDefault();

    //
    const crud_operation = e.target.value;
    const entity_name = manager.SLCT_ENTITY_NAME.get("value");

    manager.entity_field_build();
    manager.crud_constraint_build()
});


manager.BUTT_CRUD_CONSTRAINT_ADD.addEventListener('click', (e) => {
    e.preventDefault();

    //
    manager.BUTT_CRUD_CONSTRAINT_ADD.run("remove");

    const new_node_crudConstraint = manager.NODE_CRUD_CONSTRAINT();
    const new_butt_crudConstraint_add = manager.NODE_BUTT_CRUD_CONSTRAINT_ADD()

    manager.BOX_CRUD_CONSTRAINT.run("appendChild", new_node_crudConstraint);
    manager.BOX_CRUD_CONSTRAINT.run("appendChild", new_butt_crudConstraint_add);


    manager.BUTT_CRUD_CONSTRAINT_ADD.init();
});


manager.BUTT_FORM_CRUD_SUBMIT.addEventListener('click', (e) => {
    e.preventDefault();

    //
    console.log('submited forms!');
});


//
manager.entity_field_build();
manager.crud_constraint_build();
