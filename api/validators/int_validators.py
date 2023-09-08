from api.validators.validator import ValidationResult, Validator



class IntValidator(Validator):
    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value, int):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be an integer, but found type '{type(value)}'")
        return ValidationResult(True)



class IntRangeValidator(Validator):

    lo: int = None
    hi: int = None

    def __init__(self, lo: int, hi: int):
        self.lo, self.hi = lo, hi

    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value, int):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be an integer, but found type '{type(value)}'.")
        if not self.lo <= value <= self.hi:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be between {self.lo} and {self.hi} (inclusive), but found {value}.")
        return ValidationResult(True)



class HexValidator(Validator):
    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value, int):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be an integer, but found type '{type(value)}'.")
        if not 0 <= value <= 15:
            return ValidationResult(False,
                                    f"Argument Argument '{arg_name}' has to be between 0 and 15 (inclusive), but found {value}.")
        return ValidationResult(True)



class IntSetValidator(Validator):

    valid_integers: set[int] = None

    def __init__(self, valid_integers: list[int] = None):
        self.valid_integers = set(valid_integers)

    def validate(self, arg_name: str, value) -> ValidationResult:
        if not isinstance(value, int):
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be an integer, but found type '{type(value)}'.")
        if value not in self.valid_integers:
            return ValidationResult(False,
                                    f"Argument '{arg_name}' has to be one of these integers: {list(self.valid_integers).sort()} but found {value}.")
        return ValidationResult(True)