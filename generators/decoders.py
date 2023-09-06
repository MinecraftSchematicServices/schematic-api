import mcschematic

def five_hertz_y_decoder_generator(**kwargs):
    # bitCount: int = 8
    # grayCode: bool = True
    # chiseledBookshelves: bool = True
    print("kwargs", kwargs)
    bitCount: int = kwargs.get("bit_count", 8)
    grayCode: bool = kwargs.get("gray_code", True)
    chiseledBookshelves: bool = kwargs.get("chiseled_bookshelves", True)
    print("bitCount", bitCount)
    print("grayCode", grayCode)
    print("chiseledBookshelves", chiseledBookshelves)

    ## Building
    schem: mcschematic.MCSchematic = mcschematic.MCSchematic()

    for y in range(0, 2**bitCount*2, 2):
        index: int = y//2 if not grayCode else y//2 ^ (y//2 >> 1)
        for bitIndex in range(bitCount):
            bit: int = (index >> bitIndex) & 0b1
            z: int = bitIndex * 2

            if bit == 0:
                schem.setBlock((0, y, z), "minecraft:repeater[delay=2,facing=west,locked=false,powered=false]")
                schem.setBlock((0, y-1, z), "minecraft:gray_concrete")
                schem.setBlock((1, y-1, z), "minecraft:gray_concrete")
                schem.setBlock((1, y, z), "minecraft:gray_concrete")
                schem.setBlock((-1, y - 1, z), "minecraft:gray_concrete")
                schem.setBlock((-1, y, z), "minecraft:gray_concrete")
                ## Redstone OR line
                schem.setBlock((2, y-1, z), "minecraft:gray_concrete")
                schem.setBlock((2, y, z), "minecraft:redstone_wire")
                schem.setBlock((2, y-1, z-1), "minecraft:gray_concrete")
                schem.setBlock((2, y, z-1), "minecraft:redstone_wire")

            elif bit == 1:
                ## Power source
                if chiseledBookshelves:
                    schem.setBlock((0, y, z+1), "minecraft:chiseled_bookshelf[facing=west]{last_interacted_slot:14}")
                else:
                    ## Use barrels
                    schem.setBlock((0, y, z), mcschematic.BlockDataDB.SS_BARREL15)

                schem.setBlock((0, y, z), "minecraft:comparator[facing=south,mode=subtract,powered=true]{OutputSignal:15}")

                ## Block in front of comparators if none
                if schem.getBlockStateAt((0, y, z-1)) == "minecraft:air":
                    schem.setBlock((0, y, z-1), "minecraft:gray_concrete")
                    schem.setBlock((0, y-1, z-1), "minecraft:gray_concrete")

                schem.setBlock((0, y-1, z), "minecraft:gray_concrete")
                schem.setBlock((0, y-1, z+1), "minecraft:gray_concrete")
                schem.setBlock((-1, y-1, z), "minecraft:gray_concrete")
                schem.setBlock((-1, y, z), "minecraft:repeater[delay=1,facing=west,locked=false,powered=false]")

                ## Redstone OR Line
                schem.setBlock((1, y-1, z-1), "minecraft:gray_concrete")
                schem.setBlock((1, y, z-1), "minecraft:redstone_wire")
                schem.setBlock((2, y-1, z-1), "minecraft:gray_concrete")
                schem.setBlock((2, y, z-1), "minecraft:redstone_wire")
                if bitIndex != 0:
                    schem.setBlock((2, y-1, z-2), "minecraft:gray_concrete")
                    schem.setBlock((2, y, z-2), "minecraft:redstone_wire")
                if bitIndex != (bitCount-1):
                    schem.setBlock((2, y-1, z), "minecraft:gray_concrete")
                    schem.setBlock((2, y, z), "minecraft:redstone_wire")

            ## Glass towers
            if y % 7 == 0:
                ## Tower repetition
                schem.setBlock((-2, y, z), "minecraft:redstone_wire")
                schem.setBlock((-2, y-1, z), "minecraft:lime_stained_glass")
                schem.setBlock((-3, y+1, z), "minecraft:redstone_wire")
                schem.setBlock((-3, y, z), "minecraft:gray_concrete")
                schem.setBlock((-4, y-1, z), "minecraft:repeater[delay=1,facing=east,locked=false,powered=false]")
                schem.setBlock((-4, y-2, z), "minecraft:gray_concrete")
                schem.setBlock((-5, y, z), "minecraft:redstone_wire")
                schem.setBlock((-5, y-1, z), "minecraft:gray_concrete")
                schem.setBlock((-4, y+1, z), "minecraft:redstone_wire")
                schem.setBlock((-4, y, z), "minecraft:gray_concrete")
            else:
                ## No repetition
                schem.setBlock((-2, y, z), "minecraft:redstone_wire")
                schem.setBlock((-2, y-1, z), "minecraft:lime_stained_glass")
                schem.setBlock((-3, y+1, z), "minecraft:redstone_wire")
                schem.setBlock((-3, y, z), "minecraft:lime_stained_glass")
    return schem


def test(**kwargs):
    schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
    schem.setBlock((0, 0, 0), "minecraft:stone")
    return schem
