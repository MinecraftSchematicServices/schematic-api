

### === integer vector utils

IVec = tuple[int, int, int]


def ivec_add(ivec1: IVec, ivec2: IVec) -> IVec:
    return tuple(a + b for a, b in zip(ivec1, ivec2))

def translate(ivec1: IVec, ivec2: IVec) -> IVec:
    return ivec_add(ivec1, ivec2)

def translate_x(ivec1: IVec, x_offset: int) -> IVec:
    return ivec_add(ivec1, (x_offset, 0, 0))
def translate_y(ivec1: IVec, y_offset: int) -> IVec:
    return ivec_add(ivec1, (0, y_offset, 0))
def translate_z(ivec1: IVec, z_offset: int) -> IVec:
    return ivec_add(ivec1, (0, 0, z_offset))

def up(ivec: IVec, amount:int = 1) -> IVec:
    return translate_y(ivec, amount)
def down(ivec: IVec, amount:int = 1) -> IVec:
    return translate_y(ivec, -amount)

def ivec_sub(ivec1: IVec, ivec2: IVec) -> IVec:
    return tuple(a - b for a, b in zip(ivec1, ivec2))

def ivec_mul(ivec1: IVec, ivec2: IVec) -> IVec:
    return tuple(a * b for a, b in zip(ivec1, ivec2))

def ivec_div(ivec1: IVec, ivec2: IVec) -> IVec:
    return tuple(a // b for a, b in zip(ivec1, ivec2))

### ===
