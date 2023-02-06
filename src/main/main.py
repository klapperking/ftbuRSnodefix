import anvil
import argparse
from python_nbt.nbt import read_from_nbt_file, write_to_nbt_file
from os.path import join

import util.darkere_coord_from_int as darkere
from util.node_remover import remove_nodes
from util.settings import DATA_PATH
from util.get_nodes import get_rs_nodes
from util.get_region_files import coordinates_to_region_naming, get_region_names


def main(block_to_fix: str, coordinate_range: list):
    # 1. Open nbt-file using python-nbt
    nbt_file = read_from_nbt_file(DATA_PATH + "world/data/refinedstorage_nodes.dat")
    print("Read nbt-file")

    # 2. get all nodes from the nbt-file that interest us
    nodes = get_rs_nodes(nbt_file, node_type=block_to_fix)

    # 3. extract x,y,z coordinates for node-locations
    blocks_to_check = [(darkere.from_long(node)) for node in nodes]
    print("Extracted block")

    # 4. Get region-files to find specified coordinates in
    # region path
    region_loc = DATA_PATH + "world/region/"

    # get all region-filenames that need to be opened
    region_naming_range = coordinates_to_region_naming(coordinate_range)

    region_name_numbers = get_region_names(region_naming_range)

    to_fix = []
    total_node_fixes = 0

    for count, (region_x_piece, region_z_piece) in enumerate(region_name_numbers):
        print(f"Searching region file {count} of {len(region_name_numbers)}")
        fix_block_counter = 0
        # construct region fiel path and read region file using anvil module
        region_file_name = f"r.{region_x_piece}.{region_z_piece}.mca"
        region = anvil.Region.from_file(region_loc + region_file_name)

        # iterate all chunk in region
        for i in range(0, 32):
            for j in range(0, 32):

                chunk_x_range = (coordinate_range[0][0] + i * 16, coordinate_range[0][0] + (i + 1) * 16 - 1)
                chunk_z_range = (coordinate_range[0][1] + j * 16, coordinate_range[0][1] + (j + 1) * 16 - 1)

                # get chunk
                chunk = anvil.Chunk.from_region(region, i, j)

                # for each node-position, check block
                for x, y, z in blocks_to_check:

                    # if node not in this chunk, skip
                    if (not chunk_x_range[0] <= x <= chunk_x_range[1]) or (not chunk_z_range[0] <= z <= chunk_z_range[1]):
                        continue

                    # get block info using anvil
                    block_x = x - chunk_x_range[0]
                    block_z = z - chunk_z_range[0]

                    block_id = chunk.get_block(block_x, y, block_z).name()

                    # if node entry doesn't match actual block, node should be removed
                    if block_id != block_to_fix:
                        pos_long = darkere.to_long(x, y, z)
                        fix_block_counter += 1

                        # append long_psition to fix list
                        to_fix.append(pos_long)

        print(f"Found {fix_block_counter} Nodes to be removed in region")
        total_node_fixes += fix_block_counter

    print(f"Total nodes to remove: {total_node_fixes}")
    # remove nodes from nbt_file and write nbt file
    new_nbt_file = remove_nodes(nbt_file=nbt_file, pos_long_list=to_fix)
    write_to_nbt_file(join(DATA_PATH, 'world/data/refinedstorage_nodes_NEW.dat'), new_nbt_file)
    print("Done removing")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fixblock', type=str, action="store")
    parser.add_argument('-s', '--startcoordinates', type=int, nargs=2, action='append')
    parser.add_argument('-e', '--endcoordinates', type=int, nargs=2, action="append")

    fix_blocks = parser.parse_args().fixblock

    start_x_z = tuple(parser.parse_args().startcoordinates[0])
    end_x_z = tuple(parser.parse_args().endcoordinates[0])
    coordinate_range = [start_x_z, end_x_z]

    main(fix_blocks, coordinate_range)