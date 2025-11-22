ANSI_COLOR_RED = '\033[91m'
ANSI_COLOR_NULL = '\033[0m'

## Message
class Message():
    def __init__(self, type:str, content:str):
        self.type = type
        self.content = content

    @property
    def json(self)->dict:
        return {
            "content": self.content,
            "type": self.type
        }

##
class Error():
    js_class="log_message_erro"

    def print(func_name:str, e:object)->None:
        print(f"{func_name} {ANSI_COLOR_RED}ERROR{ANSI_COLOR_NULL}: {e}")

class Success():
    js_class = "log_message_ok"

## Captcha
class Captcha():
    class Error(Error):
        invalid = "Invalid Captcha"
        not_requested = "Captcha not requested"

    class Success(Success):
        ok = "Valid captcha"

## Request
class Request():
    class Error(Error):
        internal = "Something goes wrong"

        invalid_method = "Method not allow"
        invalid_fields = "Invalid fields"

        missing_fields = "Missing fields"
        empty_fields = "Please, fill all required fields"

        def invalid_client_behavior(timestamp):
            import time

            date = time.localtime(timestamp)

            return f"Because of your behavior, you cannot try sign after {date.tm_hour}:{date.tm_min}:{date.tm_sec}"

## Login
class Login():
    class Error(Error):
        user_not_found = "User not found"
        incorrect_password = "User password incorrect"

        invalid_captcha = "Invalid catpcha"

    class Request(Request):
        pass

    class Success(Success):
        pass
