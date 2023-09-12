from api.resources import constants
from api.registering.validators.validator import Validator, ValidationResult



class StringValidator(Validator):
    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value, str):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' must be a string, but found type '{type(value)}'.")
        return ValidationResult(True)



class ColorValidator(Validator):

    _string_validator = StringValidator()

    def validate(self, arg_name: str, value) -> ValidationResult:

        string_validation: ValidationResult = self._string_validator.validate(arg_name, value)
        if not string_validation.valid: return string_validation

        if value not in constants.MINECRAFT_COLORS:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be one of these colors: {constants.MINECRAFT_COLORS}, but found '{value}'.")
        return ValidationResult(True)



class ColoredSolidValidator(Validator):

    _string_validator = StringValidator()

    def validate(self, arg_name: str, value) -> ValidationResult:

        string_validation: ValidationResult = self._string_validator.validate(arg_name, value)
        if not string_validation.valid: return string_validation

        if value not in constants.COLORED_SOLID_BLOCKS:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be one of these colored solids: {constants.COLORED_SOLID_BLOCKS}, but found '{value}'.")
        return ValidationResult(True)



class StringSetValidator(Validator):

    _string_validator = StringValidator()
    valid_strings: set[str] = None

    def __init__(self, valid_strings: list[str] = None):
        self.valid_strings = set(valid_strings)

    def validate(self, arg_name: str, value) -> ValidationResult:

        string_validation: ValidationResult = self._string_validator.validate(arg_name, value)
        if not string_validation.valid: return string_validation

        if value not in self.valid_strings:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be one of these strings: {list(self.valid_strings)} but found '{value}'.")
        return ValidationResult(True)