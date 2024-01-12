import builtins

from typing import List


class DfException(builtins.Exception):
    CODE = -999999
    MESSAGE = "Server Error"

    def data(self):
        # if overriding, make sure the result is json-serializable.
        return {
            "type": self.__class__.__name__,
            "message": str(self),
        }


class DfRuntimeException(RuntimeError, DfException):
    CODE = 10001
    MESSAGE = "Runtime error"


class DfJSONValidationException(DfRuntimeException):
    CODE = 10101
    MESSAGE = "JSON Validation Error"

    def __init__(self, object_type: str, check: str, fields_checked: List[str]) -> None:
        self.object_type = object_type
        self.check = check
        self.fields_checked = fields_checked
        self.fields_checked_str = ''
        if len(self.fields_checked) == 1: self.fields_checked_str = self.fields_checked[0]
        if len(self.fields_checked) > 1: ', '.join(self.fields_checked)
        self.message = check + ' for type (' + object_type + ') : ' + self.fields_checked_str

    ####################################################################
    ##                     Generic exceptions                         ##
    ####################################################################

    ####################################################################
    ##                     Argument exceptions                        ##
    ####################################################################

    '''
        Mandatory argument not provided
        Missing argument
    '''


class ArgumentException(DfRuntimeException):
    CODE = 10001
    MESSAGE = "Argument Exception"


class MissingMandatoryArgumentException(ArgumentException):
    CODE = 10002
    MESSAGE = "Missing Mandatory Argument Exception"

    def __init__(self, object_type: type, method_name: str, argument_name: str) -> None:
        self.message = f"Missing mandatory argument '{argument_name}' on call of method {method_name} on {object_type.__name__}"


class InvalidTypeArgumentException(ArgumentException):
    CODE = 10003
    MESSAGE = "Invalid Type Argument Exception"

    def __init__(self, object_type: type, method_name: str, argument_name: str, arg_expected_type: type,
                 arg_type: type) -> None:
        self.message = f"Invalid type for argument '{argument_name}' on call of method {method_name} on {object_type.__name__}. " + \
                       f"The expected type of the argument is {str(arg_expected_type)} but the argument type was {str(arg_type)}"

    ####################################################################
    ##                 Implementation exceptions                      ##
    ####################################################################


class ImplementationException(DfRuntimeException):
    CODE = 10101
    MESSAGE = "Implementation Exception"


class NotImplementedMethodException(DfRuntimeException):
    CODE = 10102
    MESSAGE = "Method Missing Implementation Exception"

    def __init__(self, obj_class, method_name: type) -> None:
        self.message = f"The {method_name} method is not implemented for class : {str(type(obj_class))}"

    ####################################################################
    ##                       File exceptions                          ##
    ####################################################################


class NoFileAtLocationException(DfRuntimeException):
    CODE = 11001
    MESSAGE = "No file available at location"

    def __init__(self, file_path: str) -> None:
        self.message = 'No file available at location : ' + file_path


####################################################################
##                     Structure exceptions                       ##
####################################################################

class FieldRemovalException(DfRuntimeException):
    CODE = 20001
    MESSAGE = "Field Removal Exception"

    def __init__(self, field_name: str, structure_name: str) -> None:
        self.message = f"Issue during the removal of the field {field_name} on structure {structure_name}"


class FieldAdditionException(DfRuntimeException):
    CODE = 20002
    MESSAGE = "Field Addition Exception"

    def __init__(self, field_name: str, structure_name: str) -> None:
        self.message = (f"Issue during the addition of the field {field_name} on structure {structure_name} (check log "
                        f"for more information)")


####################################################################
##                    Connection exceptions                       ##
####################################################################

class NoConnectionAvailableException(DfRuntimeException):
    CODE = 30001
    MESSAGE = "No Connection Available Exception"

    def __init__(self, connection_name: str) -> None:
        self.message = f"No connection is available for name : '{connection_name}'"


class ConnectionAlreadyAvailableException(DfRuntimeException):
    CODE = 30002
    MESSAGE = "Connection Is Already Available Exception"

    def __init__(self, connection_name: str) -> None:
        self.message = f"The connection is already available for for name : '{connection_name}'"


class QueryExecutionException(DfRuntimeException):
    CODE = 30011
    MESSAGE = "Query Execution Exception"

    def __init__(self, error_message: str) -> None:
        self.message = f"{error_message}"


class RequestOnClosedConnectionException(DfRuntimeException):
    CODE = 30101
    MESSAGE = "Request on closed connection Exception"

    def __init__(self, connection_name: str, request_desc: str) -> None:
        self.message = (f"A request '{request_desc}' was done on the non-opened connection {connection_name}. Ensure "
                        f"connection is opened.")
