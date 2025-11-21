from begin.xtensions import *
from database import *

##
def register_app(app:object)->None:

    @app.route("/view/login")
    def view_login()->object:
        return flask.render_template("login.html")

    @app.route("/auth/login")
    def auth_login()->object:
        from begin.globals import Cookie

        ##
        return '{}'
