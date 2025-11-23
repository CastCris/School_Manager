from database.session import Base

##
class Person(Base):
    __tablename__ = 'Person'

    PERMISSION_MANAGER_PERSON = 1
    PERMISSION_MANAGER_REGISTER = 2
    PERMISSION_MANAGER_LOCALWORK = 4
    PERMISSION_MANAGER_DEPARTAMENT = 8
    PERMISSION_MANAGER_TASK = 16

    DEFAULT_permission = 0

    ##
    def __init__(self, **kwargs)->None:
        from begin.globals import Token, Class
        
        ##
        Class.init_from_kwargs(self, **kwargs)

        password_hashed = Token.crypt_phash(kwargs["password"])
        self.password = password_hashed

    #
    def password_auth(self, password_input:str)->bool:
        from begin.globals import Token
        from database import model_get

        ##
        password = model_get(self, "password")[0]

        return Token.crypt_phash_auth(password, password_input)

    def get_permissions_name(self)->set:
        from database import model_get

        ##
        permissions_value = model_get(self, "permissions")[0]

        permissions_allow = set()
        permissions_allow_name = set()
        itr = 0

        while permissions_value:
            permissions_allow.add((2 ** itr) if permissions_value % 2 else 0)
            permissions_value //= 2
            itr += 1

        # print('permissons: ', permissions_value, permissions_allow)

        for i in Person.__dict__.keys():
            if not i.startswith('PERMISSION_'):
                continue

            permission_value = Person.__dict__[i]
            if permission_value in permissions_allow:
                permissions_allow_name.add(i)

        return permissions_allow_name
