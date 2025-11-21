from begin.xtensions import flask

##
def register_app(app:object)->None:

    @app.route('/')
    def index()->object:
        if "user_name" in flask.request.cookies.keys():
            return "Hello!"

        return flask.redirect("/view/login")
