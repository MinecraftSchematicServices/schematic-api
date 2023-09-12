from api.registering.validators.int_validators import IntValidator
from api.registering.validators.validator import Validator, ValidationResult, ValidationError


class ArrayValidator(Validator):

    _per_item_validator: Validator = None

    def __init__(self, item_validator: Validator):
        self._per_item_validator = item_validator

    def validate(self, arg_name: str, value) -> ValidationResult:

        if not isinstance(value, list):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' must be a list.")

        for item_index, item in enumerate(value):
            item_validation: ValidationResult = self._per_item_validator.validate(f"{arg_name}[item_index={item_index}]", item)
            if not item_validation.valid:
                return item_validation

        return ValidationResult(True)