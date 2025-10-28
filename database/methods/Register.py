from database import Base

register = Base.classes.Register

class Register(register):

    FIELD_HASHED = [ "hashed_id"
                    ]

    FIELD_CIPHER = [ "cipher_id"
                    ]
