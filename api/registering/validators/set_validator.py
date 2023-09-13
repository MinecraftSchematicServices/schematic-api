from registering.validators.int_validators import IntValidator
from registering.validators.validator import Validator, ValidationResult, ValidationError
from typing import Any


class SetValidator(Validator):

    _per_item_validator: Validator = None
    set_items: set[Any] = None
    
    def __init__(self, item_validator: Validator, set_items: set[Any]):
        self._per_item_validator = item_validator
        self.set_items = set_items
        
    def validate(self, arg_name: str, value) -> ValidationResult:
            
            if not isinstance(value, set):
                return ValidationResult(False,
                                        f"Argument '{arg_name}' must be a set.")
            
            for item_index, item in enumerate(value):
                if item not in self.set_items:
                    return ValidationResult(False,
                                            f"Argument '{arg_name}' must be one of {self.set_items}, but found '{item}'.")
                    
                item_validation: ValidationResult = self._per_item_validator.validate(f"{arg_name}[item_index={item_index}]", item)
                if not item_validation.valid:
                    return item_validation
                
                
            
            return ValidationResult(True)
        
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "set",
            "item_validator": self._per_item_validator.serialize(),
            "set_items": list(self.set_items)
        }