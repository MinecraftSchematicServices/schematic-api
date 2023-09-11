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


def register_arg(args_register_data: dict[str, dict]):
    def inner(func):
        def wrapper(**kwargs):

            args: dict[str, Any] = kwargs

            ## Validate each argument
            for arg_name, register_data in args_register_data.items():

                ## An argument is required when it doesn't have a default value; otherwise optional
                required: bool = 'default_value' not in register_data
                optional: bool = not required
                if required and (arg_name not in args.keys()):
                    raise ValueError(f"Argument '{arg_name}' is missing from the arguments dict.")
                ## Get the arg value
                arg_value: Any = None
                if optional:
                    arg_value = register_data['default_value']
                elif required:
                    arg_value = args[arg_name]

                ## Validate the argument
                if 'validator' not in register_data:
                    raise ValueError(f"Validator missing for argument '{arg_name}'")
                validator: Validator = register_data['validator']
                validationResult: ValidationResult = validator.validate(arg_name, arg_value)
                if not validationResult.valid:
                    ## Use custom error message if it exists
                    error_message: str = ""
                    if 'error_message' in register_data:
                        error_message = register_data['error_message']
                    else:
                        error_message = validationResult.error_message
                    raise ValidationError(error_message)

            func(args)

        return wrapper

    return inner