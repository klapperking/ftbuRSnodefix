import anvil
from python_nbt.nbt import read_from_nbt_file, write_to_nbt_file
from os.path import join

import util.darkere_coord_from_int as darkere
from util.node_remover import remove_nodes
from util.settings import DATA_PATH
from util.get_nodes import get_rs_nodes
from util.get_region_files import coordinates_to_region_naming, get_region_names


def main(coordinate_range: list):
    # 1. Open nbt-file using python-nbt
    nbt_file = read_from_nbt_file(DATA_PATH + "world/data/refinedstorage_nodes.dat")
    print("Read nbt-file")

    #  get nodes dictionary that holds block_id: [(x,y,z),(x,y,z)]
    nodes = get_rs_nodes(nbt_file, coord_range=coordinate_range)
    print("Extracted node-coordinates")

    # 4. Get region-files to find specified coordinates in
    # region path
    region_loc = DATA_PATH + "world/region/"

    # get all region-filenames that need to be opened
    region_naming_range = coordinates_to_region_naming(coordinate_range)
    region_name_numbers = get_region_names(region_naming_range)

    to_fix = []
    total_node_fixes = 0

    for count, (region_x_piece, region_z_piece) in enumerate(region_name_numbers):

        # construct region file path
        region_file_name = f"r.{region_x_piece}.{region_z_piece}.mca"
        print(f"Searching region file {count} of {len(region_name_numbers)} - {region_file_name}")

        # open region-file using anvil module
        region = anvil.Region.from_file(region_loc + region_file_name)
        fix_block_counter = 0

        # iterate all chunks in region
        for i in range(0, 32):
            for j in range(0, 32):

                chunk_x_range = (coordinate_range[0][0] + i * 16, coordinate_range[0][0] + (i + 1) * 16 - 1)
                chunk_z_range = (coordinate_range[0][1] + j * 16, coordinate_range[0][1] + (j + 1) * 16 - 1)

                # get chunk
                chunk = anvil.Chunk.from_region(region, i, j)

                # for each node-position, check block
                for node_block_id, coordinate_list in nodes.items():
                    for x, y, z in coordinate_list:
                        # if node not in this chunk, skip
                        if (not chunk_x_range[0] <= x <= chunk_x_range[1]) or (not chunk_z_range[0] <= z <= chunk_z_range[1]):
                            continue

                        block_x = x - chunk_x_range[0]
                        block_z = z - chunk_z_range[0]

                        # get block info using anvil
                        block = chunk.get_block(block_x, y, block_z)
                        block_id = block.name()

                        # for every type of block we are looking at check
                        if block_id != node_block_id:
                            pos_long = darkere.to_long(x, y, z)
                            to_fix.append(pos_long)
                            fix_block_counter += 1

                            nodes[node_block_id].remove((x, y, z))

        print(f"Found {fix_block_counter} Nodes to be removed in region")
        total_node_fixes += fix_block_counter

    print(f"Total nodes to remove: {total_node_fixes}")
    # remove nodes from nbt_file and write nbt file
    new_nbt_file = remove_nodes(nbt_file=nbt_file, pos_long_list=to_fix)
    write_to_nbt_file(join(DATA_PATH, 'world/data/refinedstorage_nodes_NEW.dat'), new_nbt_file)
    print("Done removing")


if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-f', '--fixblock', type=str, nargs='+')
    #parser.add_argument('-s', '--startcoordinates', type=int, nargs=2, action='append')
    #parser.add_argument('-e', '--endcoordinates', type=int, nargs=2, action="append")

    #fix_blocks = parser.parse_args().fixblock

    #start_x_z = tuple(parser.parse_args().startcoordinates[0])
    #end_x_z = tuple(parser.parse_args().endcoordinates[0])
    #coordinate_range = [start_x_z, end_x_z]

    start_cords = 5450, 0, -460
    end_cords = 5510, 256, -420
    coordinate_range = [(start_cords[0], start_cords[2]), (end_cords[0], end_cords[2])]

    main(coordinate_range)