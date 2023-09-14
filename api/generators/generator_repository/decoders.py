import mcschematic
from mcschematic import MCSchematic

from generators.generator import Generator
from registering.registering import register_args
from registering.validators.int_validators import IntRangeValidator, BoolValidator
from registering.validators.string_validators import ColorValidator, ColoredSolidValidator


class FiveHertzYDecoder(Generator):

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
            "validator": IntRangeValidator(1, 8),
            "default_value": 4,
        },
        gray_code={
            "validator": BoolValidator(),
            "default_value": True
        },
        chiseled_bookshelves={
            "validator": BoolValidator(),
            "default_value": False
        },
        glass_color={
            "validator": ColorValidator(),
            "default_value": 'white'
        },
        solid_color={
            "validator": ColorValidator(),
            "default_value": 'white'
        },
        solid={
            "validator": ColoredSolidValidator(),
            "default_value": 'concrete'
        }
    )
    def generate(**gargs) -> MCSchematic:

        ### Args
        bit_count: int = gargs['bit_count']
        gray_code, chiseled_bookshelves = gargs['gray_code'], gargs['chiseled_bookshelves']
        glass_color, solid_color = gargs['glass_color'], gargs['solid_color']
        main_block_type: str = gargs['solid']

        glass_block: str = f"minecraft:{glass_color}_stained_glass"
        main_block: str = f"minecraft:{solid_color}_{main_block_type}"

        ### Building
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()

        ## Only even Y values as there is a decoder every 2 blocks.
        maxY: int = 2 ** bit_count * 2
        for y in range(0, maxY, 2):

            decoderIndex: int = y // 2
            decoderValue: int = decoderIndex if not gray_code else decoderIndex ^ (decoderIndex >> 1)

            ## Go through each bit of the current decoder
            for bitIndex in range(bit_count):
                z: int = bitIndex * 2
                bit: int = (decoderValue >> bitIndex) & 0b1

                if bit == 0:
                    schem.setBlock((0, y, z), "minecraft:repeater[delay=2,facing=west,locked=false,powered=false]")
                    schem.setBlock((0, y - 1, z), main_block)
                    schem.setBlock((1, y - 1, z), main_block)
                    schem.setBlock((1, y, z), main_block)
                    schem.setBlock((-1, y - 1, z), main_block)
                    schem.setBlock((-1, y, z), main_block)
                    ## Redstone OR line
                    schem.setBlock((2, y - 1, z), main_block)
                    schem.setBlock((2, y, z), "minecraft:redstone_wire")
                    schem.setBlock((2, y - 1, z - 1), main_block)
                    schem.setBlock((2, y, z - 1), "minecraft:redstone_wire")

                elif bit == 1:
                    ## Power source
                    if chiseled_bookshelves:
                        schem.setBlock((0, y, z + 1),
                                       "minecraft:chiseled_bookshelf[facing=west]{last_interacted_slot:14}")
                    else:
                        ## Use barrels
                        schem.setBlock((0, y, z + 1), mcschematic.BlockDataDB.SS_BARREL15)

                    schem.setBlock((0, y, z),
                                   "minecraft:comparator[facing=south,mode=subtract,powered=true]{OutputSignal:15}")

                    ## Block in front of comparators if none
                    if schem.getBlockStateAt((0, y, z - 1)) == "minecraft:air":
                        schem.setBlock((0, y, z - 1), main_block)
                        schem.setBlock((0, y - 1, z - 1), main_block)

                    schem.setBlock((0, y - 1, z), main_block)
                    schem.setBlock((0, y - 1, z + 1), main_block)
                    schem.setBlock((-1, y - 1, z), main_block)
                    schem.setBlock((-1, y, z), "minecraft:repeater[delay=1,facing=west,locked=false,powered=false]")

                    ## Redstone OR Line
                    schem.setBlock((1, y - 1, z - 1), main_block)
                    schem.setBlock((1, y, z - 1), "minecraft:redstone_wire")
                    schem.setBlock((2, y - 1, z - 1), main_block)
                    schem.setBlock((2, y, z - 1), "minecraft:redstone_wire")
                    if bitIndex != 0:
                        schem.setBlock((2, y - 1, z - 2), main_block)
                        schem.setBlock((2, y, z - 2), "minecraft:redstone_wire")
                    if bitIndex != (bit_count - 1):
                        schem.setBlock((2, y - 1, z), main_block)
                        schem.setBlock((2, y, z), "minecraft:redstone_wire")

                ## Glass towers
                if y % 7 == 0:
                    ## Tower repetition every 7 decoders
                    schem.setBlock((-2, y, z), "minecraft:redstone_wire")
                    schem.setBlock((-2, y - 1, z), glass_block)
                    schem.setBlock((-3, y + 1, z), "minecraft:redstone_wire")
                    schem.setBlock((-3, y, z), main_block)
                    schem.setBlock((-4, y - 1, z), "minecraft:repeater[delay=1,facing=east,locked=false,powered=false]")
                    schem.setBlock((-4, y - 2, z), main_block)
                    schem.setBlock((-5, y, z), "minecraft:redstone_wire")
                    schem.setBlock((-5, y - 1, z), main_block)
                    schem.setBlock((-4, y + 1, z), "minecraft:redstone_wire")
                    schem.setBlock((-4, y, z), main_block)
                else:
                    ## No repetition if not
                    schem.setBlock((-2, y, z), "minecraft:redstone_wire")
                    schem.setBlock((-2, y - 1, z), glass_block)
                    schem.setBlock((-3, y + 1, z), "minecraft:redstone_wire")
                    schem.setBlock((-3, y, z), glass_block)

        ### Retrun
        return schem
