from database import Base

personInfos = Base.classes.PersonInfos

class PersonInfos(personInfos):

    FIELD_HASHED = [ "hashed_email"
                    ,"hasehd_phone"
                    ]

    FIELD_CIPHER = [ "cipher_email"
                    ,"cipher_phone"
                    ]
