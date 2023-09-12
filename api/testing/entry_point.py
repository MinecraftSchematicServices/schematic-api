from mcschematic import Version

from api.registering.registering import register_args
from api.registering.validators.array_validators import ArrayValidator
from api.registering.validators.int_validators import IntRangeValidator
from api.generators.decoders import FiveHertzYDecoder


class A:


    def met(self):
        pass


def a():
    pass


def main():
    FiveHertzYDecoder.generate(chiseled_bookshelves=True).save(r'C:\Users\Bananas Man\AppData\Roaming\.minecraft\config\worldedit\schematics',
                                      'test1', Version.JE_1_19_4)




if __name__ == '__main__':
    main()