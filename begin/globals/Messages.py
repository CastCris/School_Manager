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

## Error & Succcess
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
        invalid_type = "Invalid Catpcha type"
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
        invalid_password = "User password incorrect"

        invalid_captcha = "Invalid catpcha"

    class Request(Request):
        pass

    class Success(Success):
        pass

## Manager
class Manager():
    class Error(Error):
        invalid_entity = "This entity doesn't exists"

        invalid_column_name = "Invalid column name"
        invalid_data_type_for_column = lambda column_name: f"Invalid data type for column {column_name}"
        invalid_column_count = "Invalid column count for selected crud operation"

        invalid_constraint = "Invalid constraint"
        invalid_data_type_for_constraint_value = "Invalid data type for constraint "

        not_permissions_enough_to_manage_entity = "You don't have permissions enough to manage this entity"

    class Success(Success):
        ok_operation = lambda operation_name: f"Operation {operation_name} completed sucessfully!"

    class Request(Request):
        pass
