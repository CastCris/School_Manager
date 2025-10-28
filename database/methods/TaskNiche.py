from database import Base

##
taskNiche = Base.classes.TaskNiche

class TaskNiche(taskNiche):

    FIELD_HASHED = [ "hashed_id"
                    ,"hashed_name"
                    ]

    FIELD_CIPHER = [ "cipher_id"
                    ,"cipher_name"
                    ]
