from begin.globals import Token, Class

##
class Seeds():
    SEQUENCE = ['Register', 'Person']

    ##
    def __init__(self)->None:
        for i in Seeds.SEQUENCE:
            Seeds.__dict__[i].init()

    ##
    class Register():
        id = Token.code_generate()

        def init()->None:
            from database import Register, session_insert

            ##
            kwargs = Class.get_attrs(Seeds.Register)
            session_insert(Register, **kwargs)

    #
    class Person():
        id = '123'
        name = 'Welligton'
        password = 'admin'
        permissions = 31

        #
        def init()->None:
            from database import session_insert, Person

            ##
            Register = Seeds.Register
            kwargs = { **Class.get_attrs(Seeds.Person), "registerId":Register.id }

            session_insert(Person, **kwargs)
