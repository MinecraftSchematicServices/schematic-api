import abc
import dataclasses
from typing import Any


@dataclasses.dataclass
class ValidationResult:
    valid: bool
    error_message: str = ''



class Validator:
    @abc.abstractmethod
    def validate(self, arg_name: str, value) -> ValidationResult:
        pass



class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

