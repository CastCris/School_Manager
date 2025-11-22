from database.session import Base
from begin.globals import Token

import time

class Register(Base):
    __tablename__ = 'Register'

    DEFAULT_id = Token.code_generate
    DEFAULT_data_register = time.time
