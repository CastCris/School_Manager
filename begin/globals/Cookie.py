def define(response:object, name:str, value:int|str, max_age:int=60*60*24)->None:
    from begin.globals.Config import serializer

    ##
    cookie_value_dumps = serializer.dumps(value)
    response.set_cookie(name, cookie_value_dumps, secure=True, httponly=True, max_age=max_age)

def delete(response:object, name:str)->None:
    response.set_cookie(name, '', max_age=0)

def get(cookie_name:str)->object|None:
    from begin.globals.Config import serializer
    import flask

    ##

    cookie = flask.request.cookies.get(cookie_name, None)
    if cookie is None:
        return None

    data = serializer.loads(cookie)
    return data

def valid(cookie_name:str)->bool:
    from itsdangerous import BadSignature

    ##
    try:
        get(cookie_name)
        return True

    except BadSignature:
        return False
