import * as global from './globals.js'

//
export class Manager extends global.Page{
    constructor(){
        super();

        //
        this.FORM_CRUD = new global.Element({
            id: "manager_form_crud"
        });


        this.SLCT_ENTITY_NAME = new global.Element({
            id: "manager_select_entityName"
        });
        this.BOX_ENTITY_FIELD = new global.Element({
            id: "manager_box_entity"
        });
        this.ENTITY_FIELD = null;


        this.SLCT_CRUD_OPERATION = new global.Element({
            id: "manager_select_crudOperation"
        });
        this.BOX_CRUD_CONSTRAINT = new global.Element({
            id: "manager_box_crudConstraint"
        });
        this.BUTT_CRUD_CONSTRAINT_ADD = new global.Element({
            id: "manager_button_node_crudConstraint_add"
        });


        this.BUTT_FORM_CRUD_SUBMIT = new global.Element({
            id: "manager_button_form_crud_submit"
        });

        // Datas
        this.DATA_BUTT_CRUD_CONSTRAINT_ADD = () => {
            const id = `manager_button_node_crudConstraint_add`;
            const cssClass = "node_button_crudConstraint_add";
            const innerHTML = `
            Add new Constraint
            `

            return {
                "id": id,
                "classList": cssClass,
                "innerHTML": innerHTML
            };
        }

        this.DATA_BUTT_CRUD_CONSTRAINT_DEL = () => {
            const cssClass = "node_button_crudConstraint_del";
            const innerHTML = `
            X
            `

            return {
                "classList": cssClass,
                "innerHTML": innerHTML
            }
        }

        this.DATA_CRUD_CONSTRAINT = () => {
            const prefix = "node_crudConstraint";
            const node_crudConstraint_count = this.BOX_CRUD_CONSTRAINT.run("querySelectorAll", `.${prefix}`).length + 1;

            var field_names_option = '';
            for(const i of this.ENTITY_FIELD){
                field_names_option += `
                    <option value="${i.toLowerCase()}">${i}</option>
                    <br>
                `;
            }

            //
            const id = `${prefix}_${node_crudConstraint_count}`;
            const classCss = prefix;
            const innerHTML = `
            <select name="select_constraint">
                <option value="where">Where</option>
            </select>

            <select name="select_constraint_entityField">
                ${field_names_option}
            </select>

            <select name="select_constraint_operator">
                <option value="=="> == </option>
                <option value="!="> != </option>

                <option value=">"> > </otpion>
                <option value=">="> >= </option>

                <option value="<"> < </otpion>
                <option value="<="> <= </option>
            </select>

            <input type="text" name="constraint_value" placeholder="Enter with constraint value" required>
            `;

            return {
                "id": id,
                "classList": classCss,
                "innerHTML": innerHTML,

                "preifx": prefix,
                "count": node_crudConstraint_count
            };
        }

        this.NODE_CRUD_CONSTRAINT = () => {
            const node = this.create_element('div', this.DATA_CRUD_CONSTRAINT());
            const button_del = this.NODE_BUTT_CRUD_CONSTRAINT_DEL();

            node.appendChild(button_del);

            return node;
        }

        this.NODE_BUTT_CRUD_CONSTRAINT_ADD = () => {
            return this.create_element('button', this.DATA_BUTT_CRUD_CONSTRAINT_ADD());
        }

        this.NODE_BUTT_CRUD_CONSTRAINT_DEL = () => {
            const node = this.create_element('button', this.DATA_BUTT_CRUD_CONSTRAINT_DEL());
            node.addEventListener('click', (e) => {
                e.preventDefault();

                //
                const node_parent = e.target.parentNode;
                node_parent.remove();
            });

            return node;
        }
    }

    //
    async entity_field_get(entity_name){
        const json = { "entity_name": entity_name };

        const response = await fetch('/auth/manager/select/entity', {
            method: 'POST',
            headers: {'Content-Type': "application/json; charset=utf-8"},

            body: JSON.stringify(json)
        });
        const data = await response.json();
        // console.log(data);

        //
        const logs = new global.MessageLogs();

        const message = data["message"];
        const entity_fields = data["entity_fields"] || null;

        if(message != undefined){
            logs.CLEAN();
            logs.ADD();
        }

        return entity_fields;
    }


    //
    async entity_field_build(){
        const entity_name = this.SLCT_ENTITY_NAME.get("value");
        const crud_operation = this.SLCT_CRUD_OPERATION.get("value").toLowerCase();

        this.BOX_ENTITY_FIELD.set("innerHTML", '');
        this.ENTITY_FIELD = await this.entity_field_get(entity_name);

        if(crud_operation == 'delete' || crud_operation == 'select')
            return;

        if(!this.ENTITY_FIELD)
            return;


        const required = crud_operation == 'create'? "required" : "";
        for(const i of this.ENTITY_FIELD){
            this.BOX_ENTITY_FIELD.set("innerHTML", this.BOX_ENTITY_FIELD.get("innerHTML") + `
                <label>${i}</label>
                <input type="text" name="entity_field_${i}" ${required}>
                <br>
            `);
        }
    }

    crud_constraint_build(){
        const entity_name = this.SLCT_ENTITY_NAME.get("value");
        const crud_operation = this.SLCT_CRUD_OPERATION.get("value").toLowerCase();
        this.BOX_CRUD_CONSTRAINT.set("innerHTML", '');

        if(crud_operation == 'create')
            return;

        const button_add = this.NODE_BUTT_CRUD_CONSTRAINT_ADD();
        this.BOX_CRUD_CONSTRAINT.run("appendChild", button_add);
        this.BUTT_CRUD_CONSTRAINT_ADD.init();
    }
}

const manager = new Manager();
manager.init_elements();

// Select Entity Name
manager.SLCT_ENTITY_NAME.addEventListener('change', (e) => {
    e.preventDefault();

    //
    manager.entity_field_build();
    manager.crud_constraint_build();
});


// Select Crud operation
manager.SLCT_CRUD_OPERATION.addEventListener('change', (e) => {
    e.preventDefault();

    //
    const crud_operation = e.target.value;
    const entity_name = manager.SLCT_ENTITY_NAME.get("value");

    manager.entity_field_build();
    manager.crud_constraint_build()
});


// Add Crud Constraint
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


// Submit!
manager.BUTT_FORM_CRUD_SUBMIT.addEventListener('click', (e) => {
    e.preventDefault();

    //
    const formData = global.forms_validation(manager.FORM_CRUD.get_object());
    if(!formData)
        return;

    const formData_json = {
        "entity_name": formData.get("entity_name"),
        "crud_operation": formData.get("crud_operation"),

        "crud_data": {
            "entity_fields": global.fieldSetData(manager.BOX_ENTITY_FIELD.get_object()),
            "crud_constraint": global.fieldSetData(manager.BOX_CRUD_CONSTRAINT.get_object())
        }
    };

    console.log(formData_json);
    console.log(formData_json, JSON.stringify(formData_json));
    fetch('/auth/manager/CRUD', {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},

        body: JSON.stringify(formData_json),
    })
    .then(response => response.json())
    .then(data => {
        const message = data["message"];
        const result = data["result"];

        console.log(data);
    });
});


//
manager.entity_field_build();
manager.crud_constraint_build();
