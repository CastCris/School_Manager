from database import Base

##
bulletinGeneral = Base.classes.BulletinGeneral

class BulletinGeneral(bulletinGeneral):

    FIELD_HASHED = [ "hashed_id"
                    ]

    FIELD_CIPHER = [ "cipher_id"
                    ]
