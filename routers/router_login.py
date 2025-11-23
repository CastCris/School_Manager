from begin.xtensions import *
from database import *

##
def register_app(app:object)->None:

    @app.route("/display/login")
    def view_login()->object:
        return flask.render_template("login.html")

    @app.route("/auth/login", methods=['POST'])
    def auth_login()->object:
        from begin.globals import Cookie, Messages, Captcha

        ##
        if flask.request.method != 'POST':
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Login.Request.Error.invalid_method,
                    type=Messages.Error.js_class
                ).json
            })


        form = flask.request.json

        user_id = form.get("user_id", None)
        user_password = form.get("user_password", None)
        captcha_input = form.get("captcha_input", None)

        if None in [ user_id, user_password, captcha_input ]:
            return flasj.jsonify({
                'message': Messages.Message(
                    content=Messages.Login.Request.Error.missing_fields,
                    type=Messages.Error.js_class
                ).json
            })

        user_id = user_id.strip()
        user_password = user_password.strip()
        captcha_input = captcha_input.strip()

        # Captcha validation
        captcha_result = Captcha.valid(captcha_input)
        captcha_result_json = captcha_result.json
        if not captcha_result_json["valid_captcha"]:
            return captcha_result

        # User validation
        user = session_query(Person, id=user_id)
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

        if not user[0].password_auth(user_password):
            return flask.jsonify({
                'message': Messages.Message(
                    content=Messages.Login.Error.invalid_password,
                    type=error_js
                ).json
            })

        ##
        user_name = model_get(user[0], "cipher_name")[0]

        response = flask.make_response(flask.jsonify({
            "href_link": "/"
        }))
        Cookie.define(response=response, name="user_name", value=user_name, max_age=60*60*24*7)
        Cookie.define(response=response, name="user_id", value=user_id, max_age=60*60*24*7)

        return response
    
    @app.route("/auth/logout")
    def auth_logout()->object:
        from begin.globals import Cookie

        ##
        response = flask.make_response(flask.redirect('/'))
        Cookie.delete(response=response, name="user_name")

        return response
