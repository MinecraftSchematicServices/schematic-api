import abc
import ast
import inspect

from mcschematic import MCSchematic

from registering.registering import _ArgDatabase

class Generator:

    @abc.abstractmethod
    def generate(self, **kwargs) -> MCSchematic:
        pass

    @classmethod
    def get_args(cls) -> _ArgDatabase._args:
        return _ArgDatabase.get_args(f"{cls.__module__}.{cls.__qualname__}")