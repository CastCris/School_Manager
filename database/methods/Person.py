from database import Base

##
person = Base.classes.Person

class Person(person):

    FIELD_HASHED = [ "hashed_cpf"
                    ,"hashed_cep"
                    ,"hashed_name"
                    ]

    FIELD_CIPHER = [ "cipher_cpf"
                    ,"cipher_cep"
                    ,"cipher_name"
                    ]
