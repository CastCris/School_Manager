from begin.xtensions import *
from begin.globals import Config, Router

from database import *

##
def database_tst()->None:
    from begin.globals import Token

    ##
    ins = session_insert(LocalWork, name="Local_A", id="1234")
    print(ins.hashed_id)

    query_model = model_get(ins, "cipher_name", "hashed_id", "cipher_id")
    query_session = session_get(LocalWork, hashed_name=Token.crypt_sha256('Local_A'))

    print('query_model: ', query_model)
    print('query_session: ', query_session)

    model_update(query_session[0], id="6789")

    query_session = session_get(LocalWork, hashed_name=Token.crypt_sha256('Local_A'))
    query_model = model_get(query_session[0], "cipher_name", "hashed_id", "cipher_id")

    print('query_model: ', query_model)
    print('query_session: ', query_session)

##
app = flask.Flask(__name__)
app.config.from_object(Config)

Router.register(app=app)

"""
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
"""

database_tst()
