from registering.validators.validator import ValidationResult, Validator
from typing import Any


class FloatValidator(Validator):
    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value, float) and not isinstance(value, int):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be a float, but found type '{type(value)}'")
        return ValidationResult(True)
    
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "float"
        }
        
class FloatRangeValidator(Validator):

    _float_validator: FloatValidator = FloatValidator()

    low_bound: float = None
    high_bound: float = None
    step: float = None

    def __init__(self, lo: float, hi: float, step: float = 0.1):
        self.low_bound, self.high_bound, self.step = lo, hi, step

    def validate(self, arg_name: str, value) -> ValidationResult:

        float_validation: ValidationResult = self._float_validator.validate(arg_name, value)
        if not float_validation.valid: return float_validation

        if not self.low_bound <= value <= self.high_bound:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be between {self.low_bound} and {self.high_bound} (inclusive), but found {value}.")
        return ValidationResult(True)
    
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "float_range",
            "low_bound": self.low_bound,
            "high_bound": self.high_bound,
            "step": self.step
        }