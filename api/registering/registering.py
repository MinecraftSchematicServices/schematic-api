from typing import Any

from api.registering.validators.validator import ValidationResult, Validator, ValidationError



class RegisteringError(Exception):
    def __init__(self, message: str):
        super().__init__(message)



def register_args(**args_register_data: dict):

    import inspect

    stack = inspect.stack()
    the_class = stack[1][0].f_locals
    the_class_name = the_class['__module__'] + '.' + the_class['__qualname__']
    #class_module: str = the_class[1][0]
    print(the_class.__dir__())
    exec(f"{the_class_name}.bonjour = 1")

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
                if required and arg_present:
                    raise ValueError(f"Argument '{arg_name}' is missing from the arguments dict.")
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

            func(**new_args)

        return wrapper

    return inner