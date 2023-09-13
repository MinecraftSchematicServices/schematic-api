import mcschematic
from mcschematic import MCSchematic

from generators.generator import Generator
from registering.registering import register_args
from registering.validators.int_validators import IntRangeValidator, BoolValidator
from registering.validators.string_validators import ColorValidator, ColoredSolidValidator
from registering.validators.array_validators import ArrayValidator

class Test1(Generator):
    
    @staticmethod
    @register_args(
        bool_list={
            "validator": ArrayValidator(BoolValidator()),
            "default_value": [True, False, False]
        },
        block_type={
            "validator": ColoredSolidValidator(),
            "default_value": 'concrete'
        },
        true_color={
            "validator": ColorValidator(),
            "default_value": 'white'
        },
        false_color={
            "validator": ColorValidator(),
            "default_value": 'black'
        },
    )
    def generate(**kwargs) -> MCSchematic:
        true_block: str = f"minecraft:{kwargs.get('true_color')}_{kwargs.get('block_type')}"
        false_block: str = f"minecraft:{kwargs.get('false_color')}_{kwargs.get('block_type')}"
        bool_list: list[bool] = kwargs.get('bool_list')
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
        for x in range(0, len(bool_list)):
            schem.setBlock((x, 0, 0), true_block if bool_list[x] else false_block)
        
        return schem
        
        