from begin.xtensions import *

##
def register_app(app:object)->None:

    @app.route("/captcha/generate")
    def captcha_generate()->object:
        from begin.globals import Captcha, Cookie, Token
        from io import BytesIO

        ##
        captcha_instance = Captcha()
        captcha_token = Token.code_captcha()
        captcha_img = captcha_instance.generate(captcha_token)

        img_io = BytesIO()
        captcha_img.save(img_io, 'PNG')
        img_io.seek(0)

        response = flask.make_response(flask.send_file(img_io, mimetype="image/png", download_name="captcha.png"))
        Cookie.define(response=response, name="captcha_token", value=captcha_token, max_age=5*60)

        return response

    @app.route("/captcha/validity/<token>")
    def catpcha_validity(token:str)->object:
        from begin.globals import Cookie

        ##
        if Cookie.get("captcha_token") is None:
            return flask.jsonify({
                "captcha_result": False
                })

        captcha_token = Cookie.get("captcha_token")
        valid = token.strip() == captcha_token

        if not valid:
            Cookie.delete("captcha_token")

        return flask.jsonify({
            "captcha_result": valid
        })
