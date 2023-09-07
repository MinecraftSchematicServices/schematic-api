import mcschematic



def five_hertz_y_decoder(**kwargs):
    """
    Generator by Sloimay (06/09/2023) dd/mm/yyyy

    Args:
        bit_count (int): The number of bits to use in the decoder.
        gray_code (bool): Whether to use gray code or not.
        chiseled_bookshelves (bool): Whether to use chiseled bookshelves or barrels.
    Returns:
        mcschematic.MCSchematic: The generated schematic.
    """
    
    ### Args
    bitCount: int = kwargs.get("bit_count", 8)
    grayCode: bool = kwargs.get("gray_code", True)
    chiseledBookshelves: bool = kwargs.get("chiseled_bookshelves", True)

    ### Building
    schem: mcschematic.MCSchematic = mcschematic.MCSchematic()

    ## Only even Y values as there is a decoder every 2 blocks.
    maxY: int = 2**bitCount*2
    for y in range(0, 2**bitCount*2, 2):

        decoderIndex: int = y//2        
        decoderValue: int = decoderIndex if not grayCode else decoderIndex ^ (decoderIndex >> 1)

        ## Go through each bit of the current decoder
        for bitIndex in range(bitCount):
            z: int = bitIndex * 2
            bit: int = (decoderIndex >> bitIndex) & 0b1

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
                ## Tower repetition every 7 decoders
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
                ## No repetition if not
                schem.setBlock((-2, y, z), "minecraft:redstone_wire")
                schem.setBlock((-2, y-1, z), "minecraft:lime_stained_glass")
                schem.setBlock((-3, y+1, z), "minecraft:redstone_wire")
                schem.setBlock((-3, y, z), "minecraft:lime_stained_glass")
    
    ### Retrun
    return schem




def test(**kwargs):
    schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
    schem.setBlock((0, 0, 0), "minecraft:stone")
    return schem
