from begin.xtensions import flask

##
def register(app:object)->None:

    @app.route('/')
    def index()->object:
        return 'Hello World!'
