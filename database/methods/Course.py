from database import Base

##
course = Base.classes.Course

class Course(course):

    FIELD_HASHED = [ "hashed_id"
                    ,"hashed_name"
                    ]

    FIELD_CIPHER = [ "cipher_id"
                    ,"cipher_name"
                    ]
