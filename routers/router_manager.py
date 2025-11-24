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
        entity_name = entity_name

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
        entity_able = ['Person', 'Register', 'LocalWork', 'Departament', 'Task' ]
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
        CONSTRAINT_ABLE = [ 'where' ]
        CONSTRAINT_OPERATORS_ABLE = ['>', '<', '>=', '<=', '==', '!=']

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

        entity_field = crud_data["entity_fields"]
        crud_constraint = crud_data["crud_constraint"]

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
        columns_type = { i[0]:i[1] for i in model_get_columns_type(model).items() if i[0] != 'dek' }

        print('entity_field: ', entity_field)
        print('columns_type: ', columns_type)
        print('crud_constraint: ', crud_constraint)

        kwargs_create = {}
        kwargs_constraint = {}

        error_js = Messages.Error.js_class
        success_js = Messages.Success.js_class

        #
        for i in entity_field.keys():
            _, column_name = i.split(PREFIX_ENTITY_FIELD)

            if not column_name in columns_type.keys():
                return flask.jsonify({
                    'message': Messages.Message(
                        content=Messages.Manager.Error.invalid_column_name,
                        type=error_js
                    ).json
                })

            if not len(entity_field[i][0]):
                continue

            try:
                kwargs_create[column_name] = columns_type[column_name](entity_field[i][0])

            except ValueError:
                return flask.jsonify({
                    'message': Messages.Message(
                        content=Messages.Manager.Error.invalid_data_type_for_column(column_name),
                        type=error_js
                    ).json
                })

        #
        constraint_count = len(crud_constraint.get('select_constraint', []))
        for i in range(constraint_count):
            try:
                constraint_name = crud_constraint['select_constraint'][i].strip().lower()
                constraint_entityField = crud_constraint['select_constraint_entityField'][i].strip()
                constraint_operator = crud_constraint['select_constraint_operator'][i].strip()
                constraint_value = crud_constraint['constraint_value'][i].strip()

            except:
                return flask.jsonify({
                    'message': Messages.Message(
                        content=Messages.Manager.Request.Error.missing_fields,
                        type=error_js
                    ).json
                })

            if not len(constraint_name):
                break

            if  not constraint_name in CONSTRAINT_ABLE \
                or not constraint_operator in CONSTRAINT_OPERATORS_ABLE \
                or not constraint_entityField in columns_type.keys():

                return flask.jsonify({
                    'message': Messages.Message(
                        content=Messages.Manager.Error.invalid_constraint,
                        type=error_js
                    ).json
                })

            try:
                constraint_value = columns_type[constraint_entityField](constraint_value)

            except TypeError:
                return flask.jsoniy({
                    'message': Messages.Message(
                        content=Messages.Manager.Error.invalid_data_type_for_constraint_value,
                        type=error_js
                    ).json
                })

            suffix = op_comp_by_operator[constraint_operator]
            kwargs_constraint[constraint_entityField + suffix] = constraint_value

        print(kwargs_create, '\n', kwargs_constraint)

        #
        query = session_query(model, **kwargs_constraint)
        result = []

        if crud_operation == 'create':
            session_insert(model, **kwargs_create)

        if crud_operation == 'delete':
            session_delete(query)

        if crud_operation == 'update':
            session_update(query, **kwargs_create)

        if crud_operation == 'select':
            for i in query:
                result.append(model_get_columns_value(i))

        print(result)
        return flask.jsonify({
            'message': Messages.Message(
                content=Messages.Manager.Success.ok_operation('create'),
                type=success_js
            ).json,
            'query_result': result
        })
