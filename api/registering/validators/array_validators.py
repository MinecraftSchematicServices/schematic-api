from registering.validators.int_validators import IntValidator
from registering.validators.validator import Validator, ValidationResult, ValidationError
from typing import Any


class ArrayValidator(Validator):

    _per_item_validator: Validator = None

    def __init__(self, item_validator: Validator, min_length: int = 0, max_length: int = None):
        self._per_item_validator = item_validator
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, arg_name: str, value) -> ValidationResult:

        if not isinstance(value, list):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' must be a list.")
        
        if self.min_length is not None and len(value) < self.min_length:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' must have at least {self.min_length} items.")
            
        if self.max_length is not None and len(value) > self.max_length:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' must have at most {self.max_length} items.")

        for item_index, item in enumerate(value):
            item_validation: ValidationResult = self._per_item_validator.validate(f"{arg_name}[item_index={item_index}]", item)
            if not item_validation.valid:
                return item_validation

        return ValidationResult(True)
    
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "array",
            "item_validator": self._per_item_validator.serialize()
        }