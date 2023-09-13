import mcschematic
from mcschematic import MCSchematic

from generators import generator
from registering.registering import register_args
from registering.validators.int_validators import IntRangeValidator, BoolValidator
from registering.validators.string_validators import ColorValidator, ColoredSolidValidator


class FiveHertzYDecoder(generator.Generator):

    @staticmethod
    @register_args(
        bit_count={
            "validator": IntRangeValidator(0, 8),
            "default_value": 4
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
    def generate(**kwargs) -> MCSchematic:

        ### Args
        bitCount: int = kwargs.get('bit_count')
        grayCode: bool = kwargs.get('gray_code')
        chiseledBookshelves: bool = kwargs.get('chiseled_bookshelves')
        glassColor: str = kwargs.get('glass_color')
        mainColor: str = kwargs.get('solid_color')
        mainBlockType: str = kwargs.get('solid')

        glassBlock: str = f"minecraft:{glassColor}_stained_glass"
        mainBlock: str = f"minecraft:{mainColor}_{mainBlockType}"

        ### Building
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()

        ## Only even Y values as there is a decoder every 2 blocks.
        maxY: int = 2 ** bitCount * 2
        for y in range(0, maxY, 2):

            decoderIndex: int = y // 2
            decoderValue: int = decoderIndex if not grayCode else decoderIndex ^ (decoderIndex >> 1)

            ## Go through each bit of the current decoder
            for bitIndex in range(bitCount):
                z: int = bitIndex * 2
                bit: int = (decoderValue >> bitIndex) & 0b1

                if bit == 0:
                    schem.setBlock((0, y, z), "minecraft:repeater[delay=2,facing=west,locked=false,powered=false]")
                    schem.setBlock((0, y - 1, z), mainBlock)
                    schem.setBlock((1, y - 1, z), mainBlock)
                    schem.setBlock((1, y, z), mainBlock)
                    schem.setBlock((-1, y - 1, z), mainBlock)
                    schem.setBlock((-1, y, z), mainBlock)
                    ## Redstone OR line
                    schem.setBlock((2, y - 1, z), mainBlock)
                    schem.setBlock((2, y, z), "minecraft:redstone_wire")
                    schem.setBlock((2, y - 1, z - 1), mainBlock)
                    schem.setBlock((2, y, z - 1), "minecraft:redstone_wire")

                elif bit == 1:
                    ## Power source
                    if chiseledBookshelves:
                        schem.setBlock((0, y, z + 1),
                                       "minecraft:chiseled_bookshelf[facing=west]{last_interacted_slot:14}")
                    else:
                        ## Use barrels
                        schem.setBlock((0, y, z + 1), mcschematic.BlockDataDB.SS_BARREL15)

                    schem.setBlock((0, y, z),
                                   "minecraft:comparator[facing=south,mode=subtract,powered=true]{OutputSignal:15}")

                    ## Block in front of comparators if none
                    if schem.getBlockStateAt((0, y, z - 1)) == "minecraft:air":
                        schem.setBlock((0, y, z - 1), mainBlock)
                        schem.setBlock((0, y - 1, z - 1), mainBlock)

                    schem.setBlock((0, y - 1, z), mainBlock)
                    schem.setBlock((0, y - 1, z + 1), mainBlock)
                    schem.setBlock((-1, y - 1, z), mainBlock)
                    schem.setBlock((-1, y, z), "minecraft:repeater[delay=1,facing=west,locked=false,powered=false]")

                    ## Redstone OR Line
                    schem.setBlock((1, y - 1, z - 1), mainBlock)
                    schem.setBlock((1, y, z - 1), "minecraft:redstone_wire")
                    schem.setBlock((2, y - 1, z - 1), mainBlock)
                    schem.setBlock((2, y, z - 1), "minecraft:redstone_wire")
                    if bitIndex != 0:
                        schem.setBlock((2, y - 1, z - 2), mainBlock)
                        schem.setBlock((2, y, z - 2), "minecraft:redstone_wire")
                    if bitIndex != (bitCount - 1):
                        schem.setBlock((2, y - 1, z), mainBlock)
                        schem.setBlock((2, y, z), "minecraft:redstone_wire")

                ## Glass towers
                if y % 7 == 0:
                    ## Tower repetition every 7 decoders
                    schem.setBlock((-2, y, z), "minecraft:redstone_wire")
                    schem.setBlock((-2, y - 1, z), glassBlock)
                    schem.setBlock((-3, y + 1, z), "minecraft:redstone_wire")
                    schem.setBlock((-3, y, z), mainBlock)
                    schem.setBlock((-4, y - 1, z), "minecraft:repeater[delay=1,facing=east,locked=false,powered=false]")
                    schem.setBlock((-4, y - 2, z), mainBlock)
                    schem.setBlock((-5, y, z), "minecraft:redstone_wire")
                    schem.setBlock((-5, y - 1, z), mainBlock)
                    schem.setBlock((-4, y + 1, z), "minecraft:redstone_wire")
                    schem.setBlock((-4, y, z), mainBlock)
                else:
                    ## No repetition if not
                    schem.setBlock((-2, y, z), "minecraft:redstone_wire")
                    schem.setBlock((-2, y - 1, z), glassBlock)
                    schem.setBlock((-3, y + 1, z), "minecraft:redstone_wire")
                    schem.setBlock((-3, y, z), glassBlock)

        ### Retrun
        return schem
