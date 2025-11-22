from begin.xtensions import *
from database import *

##
def register_app(app:object)->None:

    @app.route("/view/login")
    def view_login()->object:
        return flask.render_template("login.html")

    @app.route("/auth/login", methods=['POST'])
    def auth_login()->object:
        from begin.globals import Cookie, Messages

        ##
        form = flask.request.json

        user_cpf = form["user_name"]
        user_password = form["user_password"]

        # User validation
        user = session_query(Person, cpf=user_cpf)
        error_js = Messages.Login.Error.js_class

        if user is None:
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Login.Error.internal,
                    type=error_js
                ).json
            })

        if not len(user):
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Login.Error.user_not_found,
                    type=error_js
                ).json
            })

        return '{}'
