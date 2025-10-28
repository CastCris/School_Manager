from database import Base

##
localWork = Base.classes.LocalWork

class LocalWork(localWork):

    FIELD_HASHED = [ "hashed_id"
                    ,"hashed_name"
                    ]

    FIELD_CIPHER = [ "cipher_id"
                    ,"cipher_name"
                    ]
