// Validations
export function forms_validation(...forms){
    const logs = new MessageLogs();
    const formData = new FormData();

    for(const i of forms){
        const form_data = new FormData(i);
        const fields_required =  document.querySelectorAll(`#${i.id} [required]`) || [];
        // console.log(form_data, fields_required);

        for(const j of fields_required){
            const field = form_data.get(j.name)
            const field_type = typeof field;

            if(field_type == "string" && field.trim())
                continue;

            if(field_type == "object" && field instanceof File && field.size)
                continue;

            logs.CLEAN();
            logs.ADD(logs.MESSAGE_ERROR_CLASS, "Please, fill all required fields");

            j.focus()

            return null;
        }

        form_data.forEach((value, key) => {
            formData.append(key, value);
        });
    }

    return formData;
}

export function captchaIMG_generate(img){
    fetch('/captcha/generate/img')
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        img.src = url;
    });
}

// Layouts / Message 
class Layout_1{
    constructor(){
        this.TAGS_NAMES = [ ...(document.getElementsByTagName("*")) ];

        this.ELEMENTS_BY_CLASS = {};
        this.ELEMENTS_BY_TAG = {};
        this.ELEMENT_BY_ID = {};

        this.TAGS_NAMES.forEach( (i) => {
            if(!(i.className in Object.keys(this.ELEMENTS_BY_CLASS)) && i.className)
                this.ELEMENTS_BY_CLASS[i.className] = [ ...(document.getElementsByClassName(i.className)) ];

            if(!(i.tagName in Object.keys(this.ELEMENTS_BY_TAG)) && i.tagName)
                this.ELEMENTS_BY_TAG[i.tagName.toLowerCase()] = [ ...(document.getElementsByTagName(i.tagName)) ];

            if(!(i.id in Object.keys(this.ELEMENT_BY_ID)) && i.id)
                this.ELEMENT_BY_ID[i.id] = document.getElementById(i.id);
        })

        //
        this.CSS_VARS = window.getComputedStyle(document.body);

        //
        this.resize_timeout;

        window.addEventListener('resize', () => {
            clearTimeout(this.resize_timeout);

            this.resize_timeout = setTimeout(() =>{
                this.set_dynamic_classNames();
            }, 200);
        });
    }

    set_dynamic_classNames(){
        const className_by_tagName= (element, prefix) => {
            return `${prefix}__${element.tagName.toLowerCase()}`
        };

        const className_by_id = (element, prefix) => {
            return `${prefix}__${element.id}`
        };

        const classNames_by_classes = (element, prefix) => {
            const classNames = [];
            const regex = new RegExp(`^${prefix}__.*`);

            for(const i of element.classList){
                if(regex.test(i)){
                    classNames.push(i);
                    continue;
                }

                classNames.push(`${prefix}__${i}`);
            }

            return classNames;
        }

        //
        const vp_ratio = this.get_screen_ratio();
        const prefixes = [ "reduce", "expand" ];
        const index = ( vp_ratio >= 1 ) + 0;

        const prefix_remove = prefixes[!index + 0];
        const prefix_add = prefixes[index];

        //
        for(const i of Object.keys(this.ELEMENTS_BY_TAG)){
            this.ELEMENTS_BY_TAG[i].forEach((j) => {
                if(j.classList.length){
                    j.classList.remove(...(classNames_by_classes(j, prefix_remove)));
                    j.classList.add(...(classNames_by_classes(j, prefix_add)));
                }

                // j.classList.remove(className_by_tagName(j, prefix_remove));
                j.classList.add(className_by_tagName(j, prefix_add));

                if(j.id){
                    // j.classList.remove(className_by_id(j, prefix_remove));
                    j.classList.add(className_by_id(j, prefix_add));
                }

            });
        }
    }

    get_screen_ratio(){
        return window.screen.width / window.screen.height;
    }
}

export class MessageLogs{
    constructor(){
        const page_layout = new Layout_1();
        const ELEMENT_BY_ID = page_layout.ELEMENT_BY_ID;

        //
        this.BOX = ELEMENT_BY_ID["message_logs"];

        this.MESSAGE_ERROR_CLASS = 'message_error';

        //
        this.CLEAN = () => {
            this.BOX.innerHTML = '';
        };

        this.ADD = (message_class, message) => {
            this.BOX.innerHTML += `
                <p class="${message_class}">${message}</p>
        `
        };
    }
}

// EventListenr | Element | Page
class EventListener {
    constructor(args) {
        this.TYPE = args["type"];
        this.FUNC = args["func"];
    }
}

class Element {
    constructor(args){
        this.ID = args["id"];
        this.EVENT_LISTENERS = args["eventsLiteners"] || [];

        this.OBJECT = args["object"];
    }

    //
    addEventListener(type, func){
        this.EVENT_LISTENERS.push(new EventListener({
            type: type,
            func: func
        }));

        if(!this.OBJECT)
            return;

        this.OBJECT.addEventListener(type, func);
    }

    //
    init(){
        this.OBJECT = document.getElementById(this.ID);
        if(!this.OBJECT)
            return;

        for(const i of this.EVENT_LISTENERS){
            console.log(this.OBJECT, i.TYPE, i.FUNC);
            this.OBJECT.addEventListener(i.TYPE, i.FUNC);
        }
    }

    set(field_name, field_value){
        this.OBJECT[field_name] = field_value;
    }

    get(field_name){
        return this.OBJECT[field_name];
    }

    get_object(){
        return this.OBJECT;
    }

    remove(){
        this.OBJECT.remove();
    }

    run(func_name, ...args){
        args = args || [];
        this.OBJECT[func_name](...args);
    }
}


class Page extends Layout_1{
    constructor(){
        super();
    }

    init_elements(){
        for(const i in this){
            if(!(this[i] instanceof Element))
                continue;

            this[i].init()
        }
    }

    create_element(tag, args){
        const new_element = document.createElement(tag);
        args = args || {};

        for(const i in args){
            new_element[i] = args[i];
        }

        return new_element;
    }

}

// Login 
export class Login extends Page{
    constructor(){
        super();

        this.FORM_CREDENTIALS = new Element({
            id:"login_form_credentials"
        });
        this.FORM_CAPTCHA = new Element({
            id:"login_form_captcha"
        });

        //
        this.IMG_CAPTCHA = new Element({
            id:"login_image_captcha"
        });
        this.BUTT_CAPTCHA_GET = new Element({
            id:"login_image_captcha_get"
        });
        this.BUTT_FORM_FINISH = new Element({
            id:"login_form_finish"
        });
    }
}

export class Manager extends Page{
    constructor(){
        super();

        //
        this.FORM_CRUD = new Element({
            id: "manager_form_crud"
        });


        this.SLCT_ENTITY_NAME = new Element({
            id: "manager_select_entityName"
        });
        this.BOX_ENTITY_FIELD = new Element({
            id: "manager_box_entity"
        });
        this.ENTITY_FIELD = null;


        this.SLCT_CRUD_OPERATION = new Element({
            id: "manager_select_crudOperation"
        });
        this.BOX_CRUD_CONSTRAINT = new Element({
            id: "manager_box_crudConstraint"
        });
        this.BUTT_CRUD_CONSTRAINT_ADD = new Element({
            id: "manager_button_node_crudConstraint_add"
        });


        this.BUTT_FORM_CRUD_SUBMIT = new Element({
            id: "manager_button_form_crud_submit"
        });

        //
        this.NODE_CRUD_CONSTRAINT = () => {
            const BOX_CRUD_CONSTRAINT = this.BOX_CRUD_CONSTRAINT.get_object();
            
            const node_crudConstraint_amount = BOX_CRUD_CONSTRAINT.querySelectorAll(`.${node_crudConstraint_class}`).length;

            const id = `manager_node_crudConstraint_${node_crudConstraint_amount}`;
            const cssClass = "node_crudConstraint";
            const innerHTML = `
            <select name="select_crudConstraint">
                <option value="where">Where</option>
            </select>
            `

            return this.create_element('div', {
                "id": id,
                "class": cssClass,
                "innerHTML": innerHTML
            });
        }

        this.NODE_BUTT_CRUD_CONSTRAINT_ADD = () => {
            const id = `manager_button_node_crudConstraint_add`;
            const cssClass = "node_crudConstraint_add";
            const innerHTML = `
            Add new Constraint
            `

            return this.create_element('button', {
                "id": id,
                "class": cssClass,
                "innerHTML": innerHTML
            });
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

        //
        const logs = new MessageLogs();

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
        this.BOX_ENTITY_FIELD.set("innerHTML", '')

        if(crud_operation == 'delete' || crud_operation == 'select')
            return;

        this.ENTITY_FIELD = await this.entity_field_get(entity_name);
        if(!this.ENTITY_FIELD)
            return;


        for(const i of this.ENTITY_FIELD){
            this.BOX_ENTITY_FIELD.set("innerHTML", this.BOX_ENTITY_FIELD.get("innerHTML") + `
                <label>${i}</label>
                <input type="text" name="entity_field_${i}">
                <br>
            `);
        }
    }

    crud_constraint_build(){
        const entity_name = this.SLCT_ENTITY_NAME.get("value");
        const crud_operation = this.SLCT_CRUD_OPERATION.get("value").toLowerCase();
        this.BOX_CRUD_CONSTRAINT.set("innerHTML", '');

        if(crud_operation == 'create' || crud_operation == 'update')
            return;

        const button_add = this.NODE_BUTT_CRUD_CONSTRAINT_ADD();
        this.BOX_CRUD_CONSTRAINT.run("appendChild", button_add);
        this.BUTT_CRUD_CONSTRAINT_ADD.init();
    }
}
