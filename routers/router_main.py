from begin.xtensions import flask
from begin.globals import Cookie

##
def register_app(app:object)->None:

    @app.before_request
    def before_request()->None:
        response = flask.make_response(flask.redirect('/'))
        session_valid = True

        for i in flask.request.cookies:
            if Cookie.valid(i):
                continue

            Cookie.delete(response=response, cookie_name=i)
            session_valid = False

        #
        if not session_valid:
            return response


    @app.route('/')
    def index()->object:
        if "user_name" in flask.request.cookies.keys():
            return "Hello!"

        return flask.redirect("/view/login")
