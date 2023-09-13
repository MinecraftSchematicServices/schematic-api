from mcschematic import Version
import os
import pathlib
import sys
working_path = str(pathlib.Path(__file__).resolve().parents[1])
sys.path.append(working_path)

from registering.registering import register_args, get_available_generators
from registering.validators.array_validators import ArrayValidator
from registering.validators.int_validators import IntRangeValidator
from generators.generator_repository.decoders import FiveHertzYDecoder


class A:


    def met(self):
        pass


def a():
    pass


def main():
    # FiveHertzYDecoder.generate(chiseled_bookshelves=True).save(r'C:\Users\Bananas Man\AppData\Roaming\.minecraft\config\worldedit\schematics',
    #                                   'test1', Version.JE_1_19_4)
    print(get_available_generators())
    print(get_available_generators())
    print(get_available_generators())
    print(get_available_generators())




if __name__ == '__main__':
    main()