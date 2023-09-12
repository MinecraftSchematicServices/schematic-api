from typing import Any
import inspect

from api.registering.validators.validator import ValidationResult, Validator, ValidationError



class RegisteringError(Exception):
    def __init__(self, message: str):
        super().__init__(message)



class _ArgDatabase:
    _args = dict[str, dict]
    _classed_args: _args = {}

    @classmethod
    def register_args(cls, class_full_name: str, args: _args):
        if class_full_name in cls._classed_args:
            raise RegisteringError(f"Arguments for class '{class_full_name}' have already been registered.")
        cls._classed_args[class_full_name] = args

    @classmethod
    def get_args(cls, class_full_name: str) -> _args:
        if class_full_name not in cls._classed_args:
            raise RegisteringError(f"Class '{class_full_name}' has not been registered yet.")
        return cls._classed_args[class_full_name]



def register_args(**args_register_data: dict):

    ## Register the arguments inside the argument database
    ## TODO: make it work only if the previous frame is a class
    frame = inspect.currentframe()
    frame_back = frame.f_back
    frame_back_locals = frame_back.f_locals
    class_module: str = frame_back_locals['__module__']
    class_name: str = frame_back_locals['__qualname__']
    class_full_name: str = f"{class_module}.{class_name}"
    _ArgDatabase.register_args(class_full_name, args_register_data)

    ## Tests to see if the data inputted in the register is correct.
    for arg_name, register_data in args_register_data.items():
        ## Test if validator is there
        if 'validator' not in register_data:
            raise RegisteringError(f"Argument '{arg_name}' is missing a validator.")
        validator: Validator = register_data['validator']
        ## Test if the eventual default value passes the validator (which it has to)
        if 'default_value' not in register_data: continue
        default_value: Any = register_data['default_value']
        validation_result: ValidationResult = validator.validate(arg_name, default_value)
        if not validation_result.valid:
            raise RegisteringError(f"The default value for argument '{arg_name}' does not get validated by the inputted validator. "
                                   f"=> ({validation_result.error_message})")

    def inner(func):

        ## Function modifying
        def wrapper(**kwargs):

            args: dict[str, Any] = kwargs

            ## The args that will actually get passed into the function
            new_args: dict[str, Any] = {}

            ## Validate each argument
            for arg_name, register_data in args_register_data.items():

                ## An argument is required when it doesn't have a default value; otherwise optional
                arg_present: bool = arg_name in args.keys()
                required: bool = 'default_value' not in register_data
                optional: bool = not required
                if required and not arg_present:
                    raise ValueError(f"Argument '{arg_name}' is missing from the arguments.")
                ## Get the arg value
                arg_value: Any = None
                if arg_present:
                    arg_value = args[arg_name]
                else:
                    if optional:
                        arg_value = register_data['default_value']

                ## Validate the argument
                if 'validator' not in register_data:
                    raise ValueError(f"Validator missing for argument '{arg_name}'")
                validator: Validator = register_data['validator']
                validation_result: ValidationResult = validator.validate(arg_name, arg_value)
                if not validation_result.valid:
                    ## Use custom error message if it exists
                    error_message: str = register_data.get('error_message', validation_result.error_message)
                    raise ValidationError(error_message)

                ## Put the arg in the new args
                new_args[arg_name] = arg_value

            return func(**new_args)

        return wrapper

    return inner