from database import Base

##
departament = Base.classes.Departament

class Departament(departament):

    FIELD_HASHED = [ "hashed_id"
                    ,"hashed_name"
                    ]

    FIELD_CIPHER = [ "cipher_id"
                    ,"cipher_name"
                    ]

