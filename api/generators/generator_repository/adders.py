import mcschematic
from mcschematic import MCSchematic, MCStructure

from generators.generator import Generator
from registering.registering import register_args
from registering.validators.int_validators import IntRangeValidator


class FiveHertzAdder(Generator):

    _metadata = {
        "category": "redstone",

        "tags": {
            "5hz",
            "cool",
            "awesome"
        }
    }



    @staticmethod
    @register_args(
        bit_count={
            'validator': IntRangeValidator(1, 1024),
            'default_value': 16
        }
    )
    def generate(**gargs) -> MCSchematic:

        bit_count: int = gargs['bit_count']

        solid: str = 'minecraft:netherite_block'
        transparent: str = 'minecraft:quartz_slab[type=top]'
        container: str = mcschematic.BlockDataDB.SS_BARREL2
        wire: str = 'minecraft:redstone_wire'
        comparator: str = 'minecraft:comparator[powered=true,mode=subtract,facing=west]'


        schem: MCSchematic = MCSchematic()
        struct: MCStructure = schem.getStructure()

        def mounted_wire(pos: tuple[int, int, int], block_under: str):
            mounted(pos, block_under, wire)

        def mounted_comp(pos: tuple[int, int, int], block_under: str):
            mounted(pos, block_under, comparator)

        def mounted(pos: tuple[int, int, int], block_under: str, block_above: str):
            schem.setBlock(pos, block_under)
            schem.setBlock((pos[0], pos[1] + 1, pos[2]), block_above)


        def first_xor(bit_index: int, y: int):
            struct.cuboidFilled(solid, (0, y, 0), (0, y, 5))
            struct.cuboidFilled(wire, (0, y, 1), (0, y, 4))
            struct.cuboidFilled(solid, (0, y, 0), (0, y+1, 0))
            struct.cuboidFilled(solid, (0, y, 5), (0, y+1, 5))
            struct.cuboidFilled(solid, (1, y, 1), (1, y, 3))
            struct.setBlock((1, 1, 1), wire)
            struct.setBlock((1, 1, 2), comparator)
            struct.setBlock((1, 1, 3), comparator)
            struct.setBlock((1, 1, 4), wire)

            struct.setBlock((1, y, 4), transparent)
            struct.setBlock((2, y, 2), transparent)
            struct.setBlock((2, y, 2), wire)
            struct.setBlock((2, y+1, 3), solid)


        for bit_index in range(bit_count):
            y: int = bit_index * 2

            first_xor(bit_index, y)


        return schem
