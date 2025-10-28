from begin.xtensions import *
from begin.globals import Config, Router

from database import *

##
app = flask.Flask(__name__)
app.config.from_object(Config)

Router.register(app=app)


print('field_cipher: ', FIELD_CIPHER(Person))
print('field_hashed: ', FIELD_HASHED(Person))

if __name__ == '__main__':
    session.reset()
    app.run(debug=True, host='0.0.0.0', port='5000')
