from api.resources import constants
from api.validators.validator import Validator, ValidationResult


class ColorValidator(Validator):
    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value,  str):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be a string, but found type '{type(value)}'.")
        if value not in constants.BLOCK_COLORS:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be one of these colors: {constants.BLOCK_COLORS}, but found '{value}'.")
        return ValidationResult(True)



class StringSetValidator(Validator):

    valid_strings: set[str] = None

    def __init__(self, valid_strings: list[str] = None):
        self.valid_strings = set(valid_strings)

    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value, str):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be a string, but found type '{type(value)}'.")
        if value not in self.valid_strings:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be one of these strings: {list(self.valid_strings)} but found '{value}'.")
        return ValidationResult(True)