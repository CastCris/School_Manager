from begin.xtensions import *
from begin.globals import Config, Router

from database import session

##
app = flask.Flask(__name__)
app.config.from_object(Config)

Router.register(app=app)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
