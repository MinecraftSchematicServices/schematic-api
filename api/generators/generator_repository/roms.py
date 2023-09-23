from typing import Callable

import mcschematic
from mcschematic import MCSchematic

from generators.generator import Generator
from registering.registering import register_args
from registering.validators.array_validators import ArrayValidator
from registering.validators.block_validators import ColoredSolidBlockValidator
from registering.validators.int_validators import IntRangeValidator, BoolValidator
from registering.validators.set_validator import SetValidator
from registering.validators.string_validators import StringValidator, StringSetValidator


## The stagger intersection functions, automatically updated if we add an entry in this dict
_stagger_intersection_functions: dict[str, Callable] = {
    'xor': lambda a, b: a != b,
    'min': min,
    'max': max,
}




class BasicROMGenerator(Generator):

    _metadata = {
        "display_name": "Basic ROM Generator",
        "authors": ["sloimay"],
    }

    @staticmethod
    @register_args(
        data={
            'validator': StringValidator(),
            'default_value': ""
        },
        base={
            'validator': IntRangeValidator(2, 16),
            'default_value': 2,
        },

        bit_width={
            'validator': IntRangeValidator(1, 1024),
            'default_value': 8
        },
        y_offsets={
            'validator': ArrayValidator(IntRangeValidator(1, 1024), min_length=1, max_length=1024),
            'default_value': [2, ],
        },

        x_word_count={
            'validator': IntRangeValidator(1, 65_536),
            'default_value': 16,
        },
        x_offsets={
            'validator': ArrayValidator(IntRangeValidator(1, 1024), min_length=1, max_length=1024),
            'default_value': [2, ],
        },
        x_stagger={
            'validator': StringSetValidator(['none', 'even', 'odd']),
            'default_value': 'none',
        },

        z_word_count={
            'validator': IntRangeValidator(1, 65_536),
            'default_value': 4,
        },
        z_offsets={
            'validator': ArrayValidator(IntRangeValidator(1, 1024), min_length=1, max_length=1024),
            'default_value': [4, ],
        },
        z_stagger={
            'validator': StringSetValidator(['none', 'even', 'odd']),
            'default_value': 'none',
        },

        invert_word={
            'validator': BoolValidator(),
            'default_value': True
        },
        solid_block_on_0={
            'validator': BoolValidator(),
            'default_value': True
        },
        solid_block={
            'validator': ColoredSolidBlockValidator(),
            'default_value': "minecraft:red_concrete"
        },
        redstone_block_on_15={
            'validator': BoolValidator(),
            'default_value': True
        },
        stagger_intersection_mode={
            'validator': StringSetValidator(list(_stagger_intersection_functions.keys())),
            'default_value': list(_stagger_intersection_functions.keys())[0],
        }
    )
    def generate(**gargs) -> MCSchematic:

        ## Arg getting

        data: str = gargs['data']
        # Cleanup data
        data = data.replace(' ', '')

        base: int = gargs['base']

        bit_width: int = gargs['bit_width']
        y_offsets: list[int] = gargs['y_offsets']

        x_word_count: int = gargs['x_word_count']
        x_offsets: list[int] = gargs['x_offsets']
        x_stagger: str = gargs['x_stagger']

        z_word_count: int = gargs['z_word_count']
        z_offsets: list[int] = gargs['z_offsets']
        z_stagger: str = gargs['z_stagger']

        invert_word: bool = gargs['invert_word']
        solid_block_on_0: bool = gargs['solid_block_on_0']
        solid_block: str = gargs['solid_block']
        redstone_block_on_15: bool = gargs['redstone_block_on_15']
        stagger_intersection_mode: str = gargs['stagger_intersection_mode']


        ## Build schem
        schem: MCSchematic = MCSchematic()

        # Setup
        x_offsets_sum: int = sum(x_offsets)
        y_offsets_sum: int = sum(y_offsets)
        z_offsets_sum: int = sum(z_offsets)

        total_data_count: int = bit_width * x_word_count * z_word_count

        stagger_intersection_function: Callable = _stagger_intersection_functions.get(stagger_intersection_mode, min)

        for data_index, data_point in enumerate(data):

            ## Stop generating if we are generating more ROM than we allow
            if data_index >= total_data_count:
                break

            ## Figure out where the block should be in the world
            # Figure out the place of this block if all bits were adjacent
            data_my: int = data_index % bit_width
            data_mx: int = (data_index // bit_width) % x_word_count
            data_mz: int = (data_index // bit_width) // x_word_count

            # From getting this "unit" representation, get the actual world position
            full_x_offset_counts: int = data_mx // len(x_offsets)
            partial_x_offset_sum: int = sum(x_offsets[:data_mx % len(x_offsets)])
            data_x: int = full_x_offset_counts * x_offsets_sum + partial_x_offset_sum

            full_z_offset_counts: int = data_mz // len(z_offsets)
            partial_z_offset_sum: int = sum(z_offsets[:data_mz % len(z_offsets)])
            data_z: int = full_z_offset_counts * z_offsets_sum + partial_z_offset_sum

            x_parity: int = data_mx % 2
            x_staggered: bool = False if x_stagger == 'none' else x_parity if x_stagger == 'odd' else 1 - x_parity
            z_parity: int = data_mz % 2
            z_staggered: bool = False if z_stagger == 'none' else z_parity if z_stagger == 'odd' else 1 - z_parity
            stagger: int = stagger_intersection_function(x_staggered, z_staggered)
            full_y_offset_counts: int = data_my // len(y_offsets)
            partial_y_offset_sum: int = sum(y_offsets[:data_my % len(y_offsets)])
            data_y: int = (-1 if invert_word else 1) * (full_y_offset_counts * y_offsets_sum + partial_y_offset_sum) + stagger

            ## Place block
            data_point = data_point.lower()
            data_character_to_int_failed: bool = False
            data_as_int: int = -1
            try:
                data_as_int = int(data_point, base)
            except:
                data_character_to_int_failed = True

            if data_character_to_int_failed:
                block = 'minecraft:sponge'
            else:
                block: str = mcschematic.BlockDataDB.BARREL.fromSS(data_as_int)
                if solid_block_on_0 and data_as_int == 0:
                    block = solid_block
                if redstone_block_on_15 and data_as_int == 15:
                    block = 'minecraft:redstone_block'

            schem.setBlock((data_x, data_y, data_z), block)


        return schem

