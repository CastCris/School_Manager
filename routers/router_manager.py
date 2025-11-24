from begin.xtensions import *
from database import *

##
def register_app(app:object)->None:

    @app.route('/view/manager')
    def view_manager()->object:
        from begin.globals import Messages, Cookie

        ##
        user_cpf = Cookie.get("user_cpf")
        user = session_query(Person, cpf=user_cpf)

        if user is None:
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Request.Error.internal,
                    type=Messages.Error.js_class
                ).json
            })

        user_permissions = user[0].get_permissions_name()

        return flask.render_template('manager.html', permissions=user_permissions)


    @app.route('/auth/manager/<entity_name>')
    def auth_manager(entity_name)->object:
        from begin.globals import Messages, Cookie

        ##
        entity_name = entity_name.strip()
        entity_name = entity_name[0].upper() + entity_name[1:].lower()

        user_id = Cookie.get("user_id")
        user = session_query(Person, id=user_id)

        if user is None:
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Request.Error.internal,
                    type=Messages.Manager.Error.js_class
                ).json,
                'manager_able': False
            })

        if not len(user):
            return flask.redirect('/')

        user_permissions = user[0].get_permissions_name()
        entity_able = ['Person', 'Register', 'Localwork', 'Departament', 'Task' ]
        error_js = Messages.Manager.Error.js_class

        if not entity_name in entity_able:
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Error.invalid_entity,
                    type=error_js
                ).json,
                'manager_able': False
            })

        if     (entity_name != 'Person' and not "PERMISSION_MANAGER_PERSON" in user_permissions) \
            or (entity_name != 'Register' and not "PERMISSION_MANAGER_REGISTER" in user_permissions) \
            or (entity_name != 'Localwork' and not "PERMISSION_MANAGER_LOCALWORK" in user_permissions) \
            or (entity_name != 'Departament' and not "PERMISSION_MANAGER_DEPARTAMENT" in user_permissions) \
            or (entity_name != 'Task ' and not "PERMISSION_MANAGER_TASK" in user_permissions):

            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Error.not_permissions_enough_to_manage_entity,
                    type=error_js
                ).json,
                'manager_able': False
            })

        return flask.jsonify({
            'manager_able': True,
            'entity_name': entity_name
        })

    @app.route('/auth/manager/select/entity', methods=['POST'])
    def auth_manager_select_enityt()->object:
        from begin.globals import Messages, Cookie, Class

        ##
        if flask.request.method != 'POST':
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Request.Error.invalid_method,
                    type=Message.Error.js_class
                ).json
            })

        form = flask.request.json
        entity_name = form.get("entity_name", None)

        if entity_name is None:
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Request.Error.missing_fields,
                    type=Message.Error.js_class
                ).json
            })

        ## Authentication
        response = auth_manager(entity_name)
        response_json = response.json
        if not response_json["manager_able"]:
            return flask.jsonify({
                'message': response_json['message']
            })

        entity_name = response_json["entity_name"]

        ## Processing
        model = get_model(entity_name)
        model_fields = [ i for i in model_get_columns_name(model) if i != "dek" ]

        return flask.jsonify({
            'entity_fields': model_fields
        })

    @app.route('/auth/manager/CRUD', methods=['POST'])
    def auth_manager_CRUD()->object:
        from begin.globals import Cookie, Messages

        ##
        if flask.request.method != 'POST':
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Request.Error.invalid_method,
                    type=Messages.Manager.Error.js_class
                ).json
            })

        PREFIX_ENTITY_FIELD = 'entity_field_'
        form = flask.request.json

        entity_name = form.get("entity_name", None)
        crud_operation = form.get("crud_operation", None)
        crud_data = form.get("crud_data", None)

        if None in [entity_name, crud_operation, crud_data]:
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Request.Error.missing_fields,
                    type=Messages.Manager.Error.js_class
                ).json
            })

        entity_name = entity_name.strip()
        crud_operation = crud_operation.strip()
        crud_data = crud_data

        ## Authentication
        response = auth_manager(entity_name)
        response_json = response.json
        # print(response_json)
        if not response_json["manager_able"]:
            return flask.jsonify({
                'message': response_json["message"]
            })

        entity_name = response_json["entity_name"]

        ## Processing
        model = get_model(entity_name)
        print(model)

        """
        columns_type = model_get_columns_type(
        kwargs = {}

        if crud_operation in ['create', 'update']:
            for i in crud_data.items():
                _, field_name = i[0].split(PREFIX_ENTITY_FIELD)
                field_value = i[1].strip()

                if not len(field_value):
                    continue

        """
