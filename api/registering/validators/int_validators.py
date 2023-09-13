from registering.validators.validator import ValidationResult, Validator
from typing import Any



class IntValidator(Validator):
    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value, int):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be an integer, but found type '{type(value)}'")
        return ValidationResult(True)
    
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "int"
        }



class IntRangeValidator(Validator):

    _int_validator: IntValidator = IntValidator()

    low_bound: int = None
    high_bound: int = None

    def __init__(self, lo: int, hi: int):
        self.low_bound, self.high_bound = lo, hi

    def validate(self, arg_name: str, value) -> ValidationResult:

        int_validation: ValidationResult = self._int_validator.validate(arg_name, value)
        if not int_validation.valid: return int_validation

        if not self.low_bound <= value <= self.high_bound:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be between {self.low_bound} and {self.high_bound} (inclusive), but found {value}.")
        return ValidationResult(True)
    
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "int_range",
            "low_bound": self.low_bound,
            "high_bound": self.high_bound
        }



class HexValidator(Validator):

    _int_validator: IntValidator = IntValidator()

    def validate(self, arg_name: str, value) -> ValidationResult:

        int_validation: ValidationResult = self._int_validator.validate(arg_name, value)
        if not int_validation.valid: return int_validation

        if not 0 <= value <= 15:
            return ValidationResult(False,
                                    f"Argument Argument '{arg_name}' has to be between 0 and 15 (inclusive), but found {value}.")
        return ValidationResult(True)
    
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "hex"
        }



class BoolValidator(Validator):

    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value, bool):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be a boolean, but found type '{type(value)}'")
        return ValidationResult(True)

    def serialize(self) -> dict[str, Any]:
        return {
            "type": "bool"
        }

class IntSetValidator(Validator):

    _int_validator: IntValidator = IntValidator()

    valid_integers: set[int] = None

    def __init__(self, valid_integers: list[int] = None):
        self.valid_integers = set(valid_integers)

    def validate(self, arg_name: str, value) -> ValidationResult:

        int_validation: ValidationResult = self._int_validator.validate(arg_name, value)
        if not int_validation.valid: return int_validation

        if value not in self.valid_integers:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be one of these integers: {list(self.valid_integers).sort()} but found {value}.")
        return ValidationResult(True)
    
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "int_set",
            "valid_integers": list(self.valid_integers)
        }