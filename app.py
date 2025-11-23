from begin.xtensions import *
from begin.globals import Config, Router, Cookie

from database import *

##
app = flask.Flask(__name__)
app.config.from_object(Config)

app.jinja_env.globals["Cookie"] = Cookie

Router.register(app=app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
