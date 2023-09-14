import random
import mcschematic
import math
from opensimplex import OpenSimplex
import numpy as np
import noise
from math import floor


from mcschematic import MCSchematic

from generators.generator import Generator
from registering.registering import register_args
from registering.validators.int_validators import IntRangeValidator, BoolValidator
from registering.validators.string_validators import ColorValidator, ColoredSolidValidator
from registering.validators.array_validators import ArrayValidator
from registering.validators.block_validators import ColoredSolidBlockValidator
from registering.validators.float_validators import FloatRangeValidator, FloatValidator

# Test1 generates a schematic with a row of blocks, each block representing a boolean value in the bool_list.
class Test1(Generator):

    @staticmethod
    @register_args(
        bool_list={
            "validator": ArrayValidator(BoolValidator(), min_length=1),
            "default_value": [True, False, True, False, True, False, True, False]
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
            "validator": ArrayValidator(ColoredSolidBlockValidator(), min_length=1),
            "default_value": ["minecraft:white_concrete"]
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
        block={
            "validator": ColoredSolidBlockValidator(),
            "default_value": "minecraft:white_concrete"  
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
        block: str = kwargs.get('block')
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
        block_set = {
            "validator": ArrayValidator(ColoredSolidBlockValidator(), min_length=2),
            "default_value": ["minecraft:white_concrete", "minecraft:black_concrete"]
        },
        board_size={
            "validator": IntRangeValidator(1, 16),
            "default_value": 8
        },
    )
    def generate(**kwargs) -> MCSchematic:
        block_set = kwargs.get('block_set')
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
    
class MandelbrotSet(Generator):

    @staticmethod
    @register_args(
        main_block={
            "validator": ColoredSolidBlockValidator(),
            "default_value": 'minecraft:black_concrete'
        },
        block_palette={
            "validator": ArrayValidator(ColoredSolidBlockValidator(), min_length=1),
            "default_value": ["minecraft:red_concrete", "minecraft:orange_concrete", "minecraft:yellow_concrete", "minecraft:lime_concrete", "minecraft:green_concrete", "minecraft:cyan_concrete", "minecraft:blue_concrete", "minecraft:purple_concrete"]
        },
        width={
            "validator": IntRangeValidator(1, 256),
            "default_value": 128
        },
        height={
            "validator": IntRangeValidator(1, 256),
            "default_value": 128
        },
        iterations={
            "validator": IntRangeValidator(1, 2000),
            "default_value": 1000
        },
        min_real={
            "validator": FloatRangeValidator(-4, 4),
            "default_value": -2.5
        },
        max_real={
            "validator": FloatRangeValidator(-4, 4),
            "default_value": 1.0
        },
        min_imaginary={
            "validator": FloatRangeValidator(-4, 4),
            "default_value": -1.25
        },
        max_imaginary={
            "validator": FloatRangeValidator(-4, 4),
            "default_value": 1.25
        },
        
    )
    def generate(**kwargs) -> MCSchematic:
        main_block: str = kwargs.get('main_block')
        block_palette: list[str] = kwargs.get('block_palette')
        width: int = kwargs.get('width')
        height: int = kwargs.get('height')
        iterations: int = kwargs.get('iterations')
        min_real: float = kwargs.get('min_real')
        max_real: float = kwargs.get('max_real')
        min_imaginary: float = kwargs.get('min_imaginary')
        max_imaginary: float = kwargs.get('max_imaginary')
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
        
        
        for x in range(width):
            for z in range(height):
                c = complex(min_real + x / width * (max_real - min_real), min_imaginary + z / height * (max_imaginary - min_imaginary))
                z_val = c
                for i in range(iterations):
                    if abs(z_val) > 2.0:
                        break 
                    z_val = z_val * z_val + c
                
                if i < iterations - 1:
                    block = block_palette[i % len(block_palette)]
                else:
                    block = main_block
                
                schem.setBlock((x, 0, z), block)
        
        return schem


class JuliaSet(Generator):

    @staticmethod
    @register_args(
        main_block={
            "validator": ColoredSolidBlockValidator(),
            "default_value": 'minecraft:black_concrete'
        },
        block_palette={
            "validator": ArrayValidator(ColoredSolidBlockValidator(), min_length=1),
            "default_value": ["minecraft:red_concrete", "minecraft:orange_concrete", "minecraft:yellow_concrete", "minecraft:lime_concrete", "minecraft:green_concrete", "minecraft:cyan_concrete", "minecraft:blue_concrete", "minecraft:purple_concrete"]
        },
        width={
            "validator": IntRangeValidator(1, 256),
            "default_value": 128
        },
        height={
            "validator": IntRangeValidator(1, 256),
            "default_value": 128
        },
        iterations={
            "validator": IntRangeValidator(1, 2000),
            "default_value": 1000
        },
        real_part={
            "validator": FloatRangeValidator(-2, 2),
            "default_value": -0.7
        },
        imaginary_part={
            "validator": FloatRangeValidator(-2, 2),
            "default_value": 0.27015
        },
        min_real={
            "validator": FloatRangeValidator(-4, 4),
            "default_value": -1.5
        },
        max_real={
            "validator": FloatRangeValidator(-4, 4),
            "default_value": 1.5
        },
        min_imaginary={
            "validator": FloatRangeValidator(-4, 4),
            "default_value": -1.5
        },
        max_imaginary={
            "validator": FloatRangeValidator(-4, 4),
            "default_value": 1.5
        },
        
    )
    def generate(**kwargs) -> MCSchematic:
        main_block: str = kwargs.get('main_block')
        block_palette: list[str] = kwargs.get('block_palette')
        width: int = kwargs.get('width')
        height: int = kwargs.get('height')
        iterations: int = kwargs.get('iterations')
        real_part: float = kwargs.get('real_part')
        imaginary_part: float = kwargs.get('imaginary_part')
        min_real: float = kwargs.get('min_real')
        max_real: float = kwargs.get('max_real')
        min_imaginary: float = kwargs.get('min_imaginary')
        max_imaginary: float = kwargs.get('max_imaginary')
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
        
        
        c = complex(real_part, imaginary_part)
        
        for x in range(width):
            for z in range(height):
                z_val = complex(min_real + x / width * (max_real - min_real), min_imaginary + z / height * (max_imaginary - min_imaginary))
                for i in range(iterations):
                    if abs(z_val) > 2.0:
                        break 
                    z_val = z_val * z_val + c
                
                if i < iterations - 1:
                    block = block_palette[i % len(block_palette)]
                else:
                    block = main_block
                
                schem.setBlock((x, 0, z), block)
        
        return schem


class CircleGenerator(Generator):

    @staticmethod
    @register_args(
        radius={
            "validator": IntRangeValidator(1, 128),
            "default_value": 10
        },
        filled={
            "validator": BoolValidator(),
            "default_value": False
        },
        block={
            "validator": ColoredSolidBlockValidator(),
            "default_value": "minecraft:white_concrete"
        },
    )
    def generate(**kwargs) -> MCSchematic:
        radius: int = kwargs.get('radius')
        filled: bool = kwargs.get('filled')
        block: str = kwargs.get('block')
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
        
        for x in range(-radius, radius + 1):
            for z in range(-radius, radius + 1):
                distance = math.sqrt(x**2 + z**2)
                if filled:
                    if distance <= radius:
                        schem.setBlock((x + radius, 0, z + radius), block)
                else:
                    if radius - 1 <= distance <= radius + 1:
                        schem.setBlock((x + radius, 0, z + radius), block)
        
        return schem
    
    

class SimplexNoise3D(Generator):

    @staticmethod
    @register_args(
        x_size={
            "validator": IntRangeValidator(1, 256),
            "default_value": 32
        },
        y_size={
            "validator": IntRangeValidator(1, 256),
            "default_value": 32
        },
        z_size={
            "validator": IntRangeValidator(1, 256),
            "default_value": 32
        },
        scale={
            "validator": FloatRangeValidator(0, 1, step=0.01),
            "default_value": 0.01
        },
        block={
            "validator": ColoredSolidBlockValidator(),
            "default_value": "minecraft:white_concrete"
        },
        iso_level={
            "validator": FloatRangeValidator(-1, 1, step=0.01),
            "default_value": 0
        },
    )
    def generate(**kwargs) -> MCSchematic:
        x_size: int = kwargs.get('x_size')
        y_size: int = kwargs.get('y_size')
        z_size: int = kwargs.get('z_size')
        scale: float = kwargs.get('scale')
        block: str = kwargs.get('block')
        iso_level: float = kwargs.get('iso_level')
        
        
        schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
        
        for x in range(x_size):
            for y in range(y_size):
                for z in range(z_size):
                    noise_val = noise.snoise3(x * scale, y * scale, z * scale)
                    if noise_val >= iso_level:
                        schem.setBlock((x, y, z), block)
                    
        return schem
    
    