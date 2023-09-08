import abc
import dataclasses




@dataclasses.dataclass
class ValidationResult:
    valid: bool
    error_message: str = ''



class Validator:
    @abc.abstractmethod
    def validate(self, arg_name: str, value) -> ValidationResult:
        pass
