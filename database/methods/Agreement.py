from database import Base

##
agreement = Base.classes.Agreement

class Agreement(agreement):

    FIELD_HASHED = [ "hashed_id"
                    ]

    FIELD_CIPHER = [ "cipher_id"
                    ]
