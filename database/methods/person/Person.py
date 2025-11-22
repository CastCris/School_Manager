from database.session import Base

##
class Person(Base):
    __tablename__ = 'Person'

    ##
    def __init__(self, **kwargs)->None:
        from begin.globals import Token, Class
        
        ##
        Class.init_from_kwargs(self, **kwargs)

        password_hashed = Token.crypt_phash(kwargs["password"])
        self.password = password_hashed

    #
    def password_auth(password_input:str)->bool:
        from database import model_get

        ##
        password = model_get(self, "password")

        return Token.crypt_phash_auth(password, password_input)
