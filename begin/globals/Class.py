def init_from_kwargs(obj:object, **kwargs)->None:
    model = type("Model", (obj.__class__, ), {})

    for i in kwargs.keys():
        if not i in model.__dict__:
            continue

        setattr(obj, i, kwargs[i])

def get_attrs(obj:object)->dict:
    return { i[0]: i[1] for i in obj.__dict__.items() if not i[0].startswith('_') }
