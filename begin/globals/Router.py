import importlib

import os
import re

##
PATH_INIT = "./routers"
FILE_IGNORE = [ "__pycache__" ]

def register(path:str=PATH_INIT, app:object=None)->None:
    if app is None:
        return

    files = os.listdir(path)

    for i in files:
        if i in FILE_IGNORE:
            continue

        file_path = f"{path}/{i}"
        file_name = i[:-3]

        if os.path.isdir(file_path):
            register(file_path, app)
            continue

        if not re.search("router_.*\.py", file_path):
            continue

        spec = importlib.util.spec_from_file_location(file_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        print(module)
        module.register(app)
