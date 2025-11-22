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
        captcha_value = Cookie.get("captcha_token")

        user_cpf = form["user_name"]
        user_password = form["user_password"]
        user_captcha = form["user_captcha"]

        # Captcha validation
        if captcha_value is None:
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Login.Captcha.Error.not_requested,
                    type=Messages.Login.Error.js_class
                ).json
            })

        if user_captcha != captcha_value:
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Login.Error.invalid_captcha,
                    type=Messages.Login.Error.js_class
                ).json
            })

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
