from mcschematic import Version
import os
import pathlib
import sys

from generators.generator import Generator
from generators.generator_repository.adders import FiveHertzAdder
from generators.generator_repository.roms import BasicROMGenerator

working_path = str(pathlib.Path(__file__).resolve().parents[1])
sys.path.append(working_path)

from registering.registering import register_args, get_available_generators, get_available_generators_json
from registering.validators.array_validators import ArrayValidator
from registering.validators.int_validators import IntRangeValidator
from generators.generator_repository.decoders import FiveHertzYDecoder

from generators.generator_utils import ivec_add


class A:


    def met(self):
        pass


def a():
    pass


def main():
    #FiveHertzYDecoder.generate(chiseled_bookshelves=False).save(r'C:\Users\Bananas Man\AppData\Roaming\.minecraft\config\worldedit\schematics',
    #                                  'test1', Version.JE_1_19_4)
    #FiveHertzYDecoder.get_metadata()
    #FiveHertzAdder.generate(bit_count=8).save(
    #    r'C:\Users\Bananas Man\AppData\Roaming\.minecraft\config\worldedit\schematics',
    #                                  'test1', Version.JE_1_19_4)

    BasicROMGenerator.generate(data='0123456789ABCDEF8Z721364778635867923576862467857862678456784'*100,
                               base=16,
                               bit_width=4,
                               x_offsets=[2,],
                               z_offsets=[2, 3, 5, 8],
                               x_word_count=16,
                               z_word_count=16,
                               x_stagger='even',
                               z_stagger='even',
                               stagger_intersection_mode='xor').save(
        r'C:\Users\Bananas Man\AppData\Roaming\.minecraft\config\worldedit\schematics',
                                      'test1', Version.JE_1_19_4)





if __name__ == '__main__':
    main()