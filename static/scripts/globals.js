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
        // console.log(type, func);
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
        for(const i of this.EVENT_LISTENERS){
            // console.log(i, this.OBJECT);
            this.OBJECT.addEventListener(i.type, i.func)
        }
    }

    set(field_name, field_value){
        this.OBJECT[field_name] = field_value;
    }

    get(field_name){
        return this.OBJECT[field_name];
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

        this.BUTT_FORM_CRUD_SUBMIT = new Element({
            id: "manager_button_form_crud_submit"
        });
    }

    build_entity_field(){
        this.BOX_ENTITY_FIELD.set("innerHTML", '')
        const crud_operation = this.SLCT_CRUD_OPERATION.get("value").toLowerCase();

        if(crud_operation == 'delele' || crud_operation == 'select')
            return;

        for(const i of this.ENTITY_FIELD){
            this.BOX_ENTITY_FIELD.set("innerHTML", this.BOX_ENTITY_FIELD.get("innerHTML") + `
                <label>${i}</label>
                <input type="text" name="entity_field_${i}">
                <br>
            `);
        }
    }

    build_crud_constraint(){}
}
