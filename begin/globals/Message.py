ANSI_COLOR_RED = "\033[91m"
ANSI_COLOR_NULL = "\033[0m"

def error(func_name:str, exception:object)->None:
    print(f"{func_name} {ANSI_COLOR_RED}ERROR{ANSI_COLOR_NULL}: {exception}")
