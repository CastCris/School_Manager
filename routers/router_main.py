from begin.xtensions import flask
from begin.globals import Cookie, Router

##
def register_app(app:object)->None:

    @app.before_request
    def before_request()->None|object:
        response = flask.make_response(flask.redirect('/'))
        session_valid = True

        for i in flask.request.cookies:
            if Cookie.valid(i):
                continue

            Cookie.delete(response=response, name=i)
            session_valid = False

        #
        if not session_valid:
            return response

        ##
        path = flask.request.path
        if not Router.exists(app, path) and not path.startswith('/static'):
            flask.abort(404)

        if path.startswith('/view') and Cookie.get("user_name") is None:
            return flask.redirect('/')


    @app.route('/')
    def index()->object:
        Cookie.get("user_name")

        if "user_name" in flask.request.cookies.keys():
            return flask.redirect('/view/index')

        return flask.redirect("/display/login")

    ##
    @app.route('/view/index')
    def view_index()->object:
        return flask.render_template('index.html')
