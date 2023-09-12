import abc
import ast
import inspect


class Generator:

    @abc.abstractmethod
    def generate(self, **kwargs):
        pass

    @classmethod
    def get_args(cls):
        # Get the source of the provided class (cls)
        class_source = inspect.getsource(cls)

        # Parse the source into an AST
        tree = ast.parse(class_source)

        # Container to store decorators and their arguments
        decorators_with_args = []

        # Look for the foo method within the AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "generate":
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call):  # Check if the decorator is a callable with arguments
                        decorator_name = decorator.func.id
                        args = [ast.dump(arg, annotate_fields=False) for arg in decorator.args]
                        kwargs = [(kw.arg, ast.dump(kw.value, annotate_fields=False)) for kw in decorator.keywords]
                        decorators_with_args.append((decorator_name, args, kwargs))
                    else:
                        decorators_with_args.append((decorator.id, [], []))
        return decorators_with_args