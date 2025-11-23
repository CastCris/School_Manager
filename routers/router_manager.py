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


    @app.route('/auth/manager', methods=['POST'])
    def auth_manager()->object:
        from begin.globals import Messages

        ##
        if flask.request.method != 'POST':
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Request.Error.invalid_method,
                    type=Messages.Error.js_class
                ).json
            })

        form = flask.request.json

        entity_name = form["entity_name"]
        crud_operation = form["crud_operation"]
        crud_constraint = form["crud_constraint"]
        entity_field = form["entity_field"]

        return '{}'

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

        entity_name = entity_name.strip().upper()

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
        entity_able = ['PERSON', 'REGISTER', 'LOCALWORK', 'DEPARTAMENT', 'TASK' ]
        error_js = Messages.Manager.Error.js_class

        if entity_name not in entity_able:
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Error.invalid_entity,
                    type=error_js
                ).json
            })
        
        #
        if     (entity_name != 'PERSON' and not "PERMISSION_MANAGER_PERSON" in user_permissions) \
            or (entity_name != 'REGISTER' and not "PERMISSION_MANAGER_REGISTER" in user_permissions) \
            or (entity_name != 'LOCALWORK' and not "PERMISSION_MANAGER_LOCALWORK" in user_permissions) \
            or (entity_name != 'DEPARTAMENT' and not "PERMISSION_MANAGER_DEPARTAMENT" in user_permissions) \
            or (entity_name != 'TASK ' and not "PERMISSION_MANAGER_TASK" in user_permissions):

            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Manager.Error.not_permissions_enough_to_manage_entity,
                    type=error_js
                ).json
            })

        ##
        model = None

        if entity_name == 'PERSON':
            model = Person
        if entity_name == 'REGISTER':
            model = Register
        if entity_name == 'LOCALWORK':
            model = LocalWork
        if entity_name == 'DEPARTAMENT':
            model = Departament
        if entity_name == 'TASK':
            model = Task

        model_fields = [ i for i in model_get_columns_name(model) if i != "dek" ]
        print(model_fields)

        return flask.jsonify({
            'entity_fields': model_fields
        })
