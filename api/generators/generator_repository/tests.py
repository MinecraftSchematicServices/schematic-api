import random
import mcschematic

from mcschematic import MCSchematic

from generators.generator import Generator
from registering.registering import register_args
from registering.validators.int_validators import IntRangeValidator, BoolValidator
from registering.validators.string_validators import ColorValidator, ColoredSolidValidator
from registering.validators.array_validators import ArrayValidator



# Test1 generates a schematic with a row of blocks, each block representing a boolean value in the bool_list.
class Test1(Generator):

    @staticmethod
    @register_args(
        bool_list={
            "validator": ArrayValidator(BoolValidator())
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
        dummy={
            "validator": IntRangeValidator(0, 0),
            "default_value": 0
        }
        
    )
    def generate(**kwargs) -> MCSchematic:
        true_block: str = f"minecraft:{kwargs.get('true_color')}_{kwargs.get('block_type')}"
        false_block: str = f"minecraft:{kwargs.get('false_color')}_{kwargs.get('block_type')}"
        bool_list: list[bool] = kwargs.get('bool_list')
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
        for x in range(0, len(bool_list)):
            schem.setBlock((x, 0, 0), true_block if bool_list[x] else false_block)
        
        return schem
        
        
# Test2 generates a NxN grid of random blocks from the block_set.
class Test2(Generator):

    @staticmethod
    @register_args(
        block_set={
            "validator": ArrayValidator(ColoredSolidValidator())
        },
        block_size={
            "validator": IntRangeValidator(1, 16),
            "default_value": 1
        },
        grid_size={
            "validator": IntRangeValidator(1, 16),
            "default_value": 1
        },
    )
    def generate(**kwargs) -> MCSchematic:
        block_set: list[str] = kwargs.get('block_set')
        block_size: int = kwargs.get('block_size')
        grid_size: int = kwargs.get('grid_size')
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
        for x in range(0, grid_size):
            for z in range(0, grid_size):
                schem.setBlock((x * block_size, 0, z * block_size), block_set[random.randint(0, len(block_set) - 1)])
        
        return schem
    
# This test will generate vertical pillars based on a given height, block type, and spacing.
class Test3(Generator):

    @staticmethod
    @register_args(
        height={
            "validator": IntRangeValidator(1, 256),
            "default_value": 5
        },
        block_type={
            "validator": ColoredSolidValidator(),
            "default_value": 'concrete'
        },
        spacing={
            "validator": IntRangeValidator(1, 16),
            "default_value": 2
        },
        pillar_count={
            "validator": IntRangeValidator(1, 16),
            "default_value": 5
        },
    )
    def generate(**kwargs) -> MCSchematic:
        block: str = f"minecraft:{kwargs.get('block_type')}"
        height: int = kwargs.get('height')
        spacing: int = kwargs.get('spacing')
        pillar_count: int = kwargs.get('pillar_count')
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
        for i in range(pillar_count):
            for y in range(height):
                schem.setBlock((i * spacing, y, 0), block)
        
        return schem

        
# This test will generate a NxN checkerboard pattern of blocks from the block_set.
class Test4(Generator):

    @staticmethod
    @register_args(
        block_set={
            "validator": ArrayValidator(ColoredSolidValidator())
        },
        board_size={
            "validator": IntRangeValidator(1, 16),
            "default_value": 8
        },
    )
    def generate(**kwargs) -> MCSchematic:
        block_set: list[str] = kwargs.get('block_set')
        board_size: int = kwargs.get('board_size')
        block1 = block_set[random.randint(0, len(block_set) - 1)]
        block2 = block_set[random.randint(0, len(block_set) - 1)]
        while block1 == block2:
            block2 = block_set[random.randint(0, len(block_set) - 1)]
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
        for x in range(board_size):
            for z in range(board_size):
                if (x + z) % 2 == 0:
                    schem.setBlock((x, 0, z), block1)
                else:
                    schem.setBlock((x, 0, z), block2)
        
        return schem
