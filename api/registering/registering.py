from typing import Any
import inspect
import os
import sys
from registering.validators.validator import ValidationResult, Validator, ValidationError
import sys 
import importlib.util

class RegisteringError(Exception):
    def __init__(self, message: str):
        super().__init__(message)



class _ArgDatabase:
    _args = dict[str, dict]
    _classed_args: _args = {}

    @classmethod
    def register_args(cls, class_full_name: str, args: _args):
        # TODO: fix this once the registering is done in a better way
        # if class_full_name in cls._classed_args:
        #     raise RegisteringError(f"Class '{class_full_name}' has already been registered.")
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

# def get_available_generators():
#     generator_classes = {}
#     relative_path = "../generators/generator_repository"
#     import_path = os.path.join(os.path.dirname(__file__), relative_path)
#     resolved_path = os.path.realpath(import_path)
#     for filename in os.listdir(resolved_path):
#         if filename.endswith(".py") and filename != "__init__.py":
#             module_name = filename[:-3]
#             print(f"Found generator module '{module_name}'")
#             module_path = os.path.join(resolved_path, filename)
#             spec = importlib.util.spec_from_file_location(module_name, module_path)
#             module = importlib.util.module_from_spec(spec)
#             spec.loader.exec_module(module)
#             for name, obj in inspect.getmembers(module):
#                 if inspect.isclass(obj) and obj.__module__ == module_name:
#                     generator_classes[name] = {}
#                     doctsring = obj.__doc__
#                     if doctsring is not None:
#                         generator_classes[name]["docstring"] = doctsring
#                     args = _ArgDatabase.get_args(f"{obj.__module__}.{obj.__qualname__}")
#                     # serialize the validators
#                     serialized_args = {}
#                     for arg_name, arg_data in args.items():
#                         serialized_args[arg_name] = {}
#                         for key, value in arg_data.items():
#                             if key == "validator":
#                                 serialized_args[arg_name][key] = value.serialize()
#                             else:
#                                 serialized_args[arg_name][key] = value
#                     generator_classes[name]["args"] = serialized_args
#     return generator_classes

# return a dict of all the available generators using the class name as key and the class object as value
# FIXME: This is a bit of a mess
def get_available_generators():
    # TODO: Do the registering in a better way so that this doesn't have to be done on each call
    generator_classes = {}
    relative_path = "../generators/generator_repository"
    import_path = os.path.join(os.path.dirname(__file__), relative_path)
    resolved_path = os.path.realpath(import_path)
    for filename in os.listdir(resolved_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = os.path.join(resolved_path, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == module_name:
                    generator_classes[name] = obj
    return generator_classes


def generators_to_json(generator_classes: dict[str, type]) -> dict[str, dict]:
    generator_classes_json = {}
    for name, obj in generator_classes.items():
        generator_classes_json[name] = {}
        doctsring = obj.__doc__
        if doctsring is not None:
            generator_classes_json[name]["docstring"] = doctsring
        args = _ArgDatabase.get_args(f"{obj.__module__}.{obj.__qualname__}")
        # serialize the validators
        serialized_args = {}
        for arg_name, arg_data in args.items():
            serialized_args[arg_name] = {}
            for key, value in arg_data.items():
                if key == "validator":
                    serialized_args[arg_name][key] = value.serialize()
                else:
                    serialized_args[arg_name][key] = value
        generator_classes_json[name]["args"] = serialized_args
    return generator_classes_json

def get_available_generators_json():
    return generators_to_json(get_available_generators())