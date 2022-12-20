import math

def main(input_long: int):
    x, y, z, = from_long(input_long)
    return x, y, z

def from_long(input_long: int):
    x = unpack_x(input_long)
    y = unpack_y(input_long)
    z = unpack_z(input_long)
    return x, y, z

def unpack_x(input_long: int) -> int:
    return input_long << (64 - field_218293_k - NUM_X_BITS) >> (64 - NUM_X_BITS)

def unpack_y(input_long: int) -> int:
    mask = (1 << NUM_Y_BITS) - 1  # create a mask with NUM_Y_BITS 1s
    return (input_long & mask) << 64 - NUM_Y_BITS >> 64 - NUM_Y_BITS

def unpack_z(input_long: int) -> int:
    input_long += 2**64
    mask = (1 << NUM_Z_BITS) - 1  # create a mask with NUM_Z_BITS 1s

    #for some reason this is not the same as in java
    return (input_long & mask) << (64 - NUM_Y_BITS - NUM_Z_BITS) >> (64 - NUM_Z_BITS)

def smallestEncompassingPowerOfTwo(value: int) -> int:
        i = value - 1
        i = i | i >> 1
        i = i | i >> 2
        i = i | i >> 4
        i = i | i >> 8
        i = i | i >> 16
        return i + 1

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


# testing
test_input = -2462081428529088
desired_out = (-8953, 64, 12470)
actual_out = main(test_input)

if not desired_out == actual_out:
    print("Not desired output: ", actual_out)

"""Problem:
unpack_z produces   0011000010110110 (Binary's signed twos complement) (binary: 11000010110110)
versus java:        1111000010110110 (Binary's signed twos complement) (binary: -111101001010)

I dont understand why this is happening - either the >> in python doesnt preserve sign bit (?)
or java long is in some way different from python int that i dont know about

"""
