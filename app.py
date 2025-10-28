from begin.xtensions import *
from begin.globals import Config, Router

from database import *

##
def database_tst()->None:
    from begin.globals import Token

    ##
    ins = session_insert(LocalWork, name="Local_A", id="1234")

    query_model = model_get(ins, "cipher_name", "hashed_id")
    query_session = session_get(LocalWork, hashed_name=Token.crypt_sha256('Local_A'))

    print('query_model: ', query_model)
    print('query_session: ', query_session)

    session_update(query_session, hashed_id="6789")
    print(Token.crypt_sha256('6789'))

    query_session = session_get(LocalWork, hasehd_id=Token.crypt_sha256('6789'))
    # query_mode = model_get(query_session[0], "hashed_id")

    # print('query_model: ', query_model)
    print('query_session: ', query_session)

##
app = flask.Flask(__name__)
app.config.from_object(Config)

Router.register(app=app)

if __name__ == '__main__':
    database_tst()

    app.run(debug=True, host='0.0.0.0', port='5000')
