import math

def from_long(input_long: int):
    x = unpack_x(input_long)
    y = unpack_y(input_long)
    z = unpack_z(input_long)
    return x, y, z

def unpack_x(input_long: int) -> int:
    mask = (1 << NUM_X_BITS) - 1
    right_shifted = input_long >> (64 - NUM_X_BITS)
    just_x = right_shifted & mask

    if (just_x & (1 << (NUM_X_BITS -1))) != 0:
        just_x = just_x - (1 << NUM_X_BITS)
    return just_x

def unpack_y(input_long: int) -> int:
    mask = (1 << NUM_Y_BITS) - 1  # create a mask with NUM_Y_BITS 1s
    return (input_long & mask) << 64 - NUM_Y_BITS >> 64 - NUM_Y_BITS

def unpack_z(input_long: int) -> int:
    mask = (1 << NUM_Z_BITS) - 1 # 26x 1 for 26 bit 2s complement
    right_shifted = input_long >> (64 - NUM_X_BITS - NUM_Z_BITS)
    just_z = right_shifted & mask

    #if sign bit is set, substract value of MSB to invert sign.
    if (just_z & (1 << (NUM_Z_BITS - 1))) != 0:
        just_z = just_z - (1 << NUM_Z_BITS)

    return just_z

def smallestEncompassingPowerOfTwo(value: int) -> int:
        i = value - 1
        i = i | i >> 1
        i = i | i >> 2
        i = i | i >> 4
        i = i | i >> 8
        i = i | i >> 16
        return i + 1

def to_long(x: int, y: int, z: int) -> int:
    """
    :param x: x coordinate
    :param y: y coordinate
    :param z: z coordinate
    :return: 64-bit integer
    """
    # Unclear why if done for x the results are wrong

    # re-invert sign bits only for z
    if (z & (1 << (NUM_Z_BITS - 1))) != 0:
        z = z + (1 << NUM_Z_BITS)

    after_x = x << NUM_Z_BITS + NUM_Y_BITS
    after_z = after_x + (z << NUM_Y_BITS)
    after_y = after_z + y
    return after_y

NUM_X_BITS = 1 + int(math.log2(smallestEncompassingPowerOfTwo(30000000))) #26
NUM_Z_BITS = NUM_X_BITS #26
NUM_Y_BITS = 64 - NUM_X_BITS - NUM_Z_BITS #12

field_218292_j = NUM_Y_BITS #12
field_218293_k = NUM_Y_BITS + NUM_Z_BITS #38

X_MASK = (1 << NUM_X_BITS) - 1
Y_MASK = (1 << NUM_Y_BITS) - 1
Z_MASK = (1 << NUM_Z_BITS) - 1
INVERSE_START_BITS_Z = NUM_Y_BITS
INVERSE_START_BITS_X = NUM_Y_BITS + NUM_Z_BITS

x = y = z = 0

"""
testing
with open("pos_long_list.txt", "r") as f:
    node_longs = f.readlines()

for i in node_longs:
    long = int(i[:-1])

    x, y, z = from_long(long)

    test = to_long(x, y, z)

    print(test, long)
"""