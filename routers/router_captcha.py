from begin.xtensions import *

##
def register_app(app:object)->None:

    @app.route("/captcha/generate/<type>")
    def captcha_generate(type:str)->object:
        from begin.globals import Captcha

        return Captcha.generate(type)
