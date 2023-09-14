from resources import constants
from registering.validators.validator import Validator, ValidationResult
from typing import Any



class ColoredSolidBlockValidator(Validator):
    def validate(self, arg_name: str, value) -> ValidationResult:
        # check if it matches the format of a colored solid block
        if not isinstance(value, str):
            return ValidationResult(False, f"{arg_name} is not a string")
        if not value.startswith("minecraft:"):
            return ValidationResult(False, f"{value} is not a valid block")
        has_valid_block = False
        has_valid_color = False
        for block in constants.COLORED_SOLID_BLOCKS:
            if block in value:
                has_valid_block = True
                block_name = block
                break
        if not has_valid_block:
            return ValidationResult(False, f"{value} is not a valid block")
        for color in constants.MINECRAFT_COLORS:
            if color in value:
                has_valid_color = True
                color_name = color
                break
        if not has_valid_color:
            return ValidationResult(False, f"{value} is not a valid color")
        # if value != f"minecraft:{color_name}_{block_name}":
        #     return ValidationResult(False, f"{value} is not a valid colored solid block {color_name}_{block_name}")
        
        return ValidationResult(True, None)
        
            
        
    
    def serialize(self) -> dict[str, Any]:
        return {
            "type": "colored_solid_block"
        }