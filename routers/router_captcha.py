from begin.xtensions import *

##
def register_app(app:object)->None:

    @app.route("/captcha/generate")
    def captcha_generate()->object:
        from begin.globals import Captcha, Cookie, Token
        from io import BytesIO

        ##
        captcha_instance = Captcha.Image()
        captcha_token = Token.code_captcha()
        captcha_img = captcha_instance.generate(captcha_token)
        # captcha_img = captcha_instance.generate('gggggg999')

        img_io = BytesIO()
        captcha_img.save(img_io, 'PNG')
        img_io.seek(0)

        #
        captcha_token_hashed = Token.crypt_phash(captcha_token)

        response = flask.make_response(flask.send_file(img_io, mimetype="image/png", download_name="captcha.png"))
        Cookie.define(response=response, name="captcha_token", value=captcha_token_hashed, max_age=5*60)

        return response

    @app.route("/captcha/valid/<token>")
    def catpcha_validity(token:str)->object:
        from begin.globals import Cookie, Messages, Token

        ##
        if Cookie.get("captcha_token") is None:
            return flask.jsonify({
                "valid_captcha": False,
                "message": Messages.Message(
                    content=Messages.Captcha.Error.not_requested,
                    type=Messages.Captcha.Error.js_class
                ).json
            })

        captcha_token = Cookie.get("captcha_token")
        valid = Token.crypt_phash_auth(captcha_token, token)
        msg = Messages.Message(
            content=Messages.Captcha.Error.invalid if not valid else Messages.Captcha.Success.ok,
            type=Messages.Captcha.Error.js_class if not valid else Messages.Captcha.Success.js_class
        ).json

        return flask.jsonify({
            "valid_captcha": valid,
            "message": msg
        })
