from python_nbt.nbt import read_from_nbt_file, NBTTagBase
import json
import darkere_coord_from_int
import anvil
import sys
import argparse


def get_rs_nodes(nbt_file, node_type: str) -> list:

    long_pos_list = []
    for node in nbt_file["data"]["Nodes"]:
        data = node["Data"]
        position = node["Pos"]
        id = node["Id"]

        # we only care about importer and exporter
        if id != node_type:
            continue

        # replace ' with " in the id string, so json.loads can read it
        pos_json = json.loads(str(position).replace("\'", "\""))
        coordinates = darkere_coord_from_int.from_long(int(pos_json["value"]))

        long_pos_list.append(pos_json["value"])

    return long_pos_list


def save_long_pos_list(long_pos_list: list, file_path: str) -> None:
    # save to file
    with open("pos_long_list.txt", "w") as out:
        for i in long_pos_list:
            out.write(str(i) + "\n")
    return None


def coordinates_to_region_naming(coordinate_range: list) -> list:

    region_naming_range = []
    for i in coordinate_range:
        new_coord_pair = []
        for j in i:
            if -512 < j < 512:
                if j < 0:
                    j = -1
                elif j > 0:
                    j = 1
            else:
                j = int(j / 16 / 32)

            new_coord_pair.append(j)
        region_naming_range.append(tuple(new_coord_pair))

    return region_naming_range

def main(block_to_fix: str, coordinate_range: list):

    nbt_file = read_from_nbt_file("../../resources/FTBU_files/world/data/refinedstorage_nodes.dat")
    nbt_json = nbt_file.json_obj(full_json=True)

    nodes = get_rs_nodes(nbt_file, node_type=block_to_fix)
    blocks_to_check = [(darkere_coord_from_int.from_long(node)) for node in nodes]

    """
    blocks_to_check = []
    # TODO Replace with opening region file
    with open("pos_long_list.txt", "r") as f:
        nodes = [int(line) for line in f.readlines()]
    for node in nodes:
        x, y, z = darkere_coord_from_int.from_long(node)
        blocks_to_check.append((x, y, z))
    """

    region_loc = "../../resources/FTBU_files/world/region/"
    region_naming_range = coordinates_to_region_naming(coordinate_range)

    start_region_path = f"r.{region_naming_range[0][0]}.{region_naming_range[0][1]}.mca"
    end_region_path = f"r.{region_naming_range[1][0]}.{region_naming_range[1][1]}.mca"

    # TODO Multiple relevant regions!
    if not start_region_path == end_region_path:
        pass

    to_fix = []

    region = anvil.Region.from_file(region_loc + start_region_path)
    # main loop for all chunks in the region
    for i in range(0, 32):
        for j in range(0, 32):
            # get x and z range in the active chunk
            x_range = (coordinate_range[0][0] + i * 16, coordinate_range[0][0] + (i + 1) * 16 - 1)
            z_range = (coordinate_range[0][1] + j * 16, coordinate_range[0][1] + (j + 1) * 16 - 1)
            chunk = anvil.Chunk.from_region(region, i, j)

            # for each rs node, get the block
            for x, y, z in blocks_to_check:
                # block not in range, we ignore
                # TODO not necessary, once we read the rs nbt based on coordinate-range only
                if (not x_range[0] < x < x_range[1]) or (not z_range[0] < z < z_range[1]):
                    continue
                # if block in range get its chunk position and the compare with check-block
                else:
                    # get block position in active chunk
                    block_x = x - x_range[0]
                    block_z = z - z_range[0]

                    block_id = chunk.get_block(block_x, y, block_z).name()

                    # if node entry doesn't match chunk block, node should be removed
                    if block_id != block_to_fix:
                        pos_long = darkere_coord_from_int.to_long(x, y, z)
                        print(f"Node at {x, y, z}; {pos_long} is not {block_to_fix} but {block_id}")

                        to_fix.append((x, y, z))
    """
    #save the block position to remove to a txt file
    with open(str(block_to_fix) + ".txt", "a+") as f:
    """

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fixblock', action="store")
    parser.add_argument('-s', '--startcoordinates', type=int, nargs=2, action='append')
    parser.add_argument('-e', '--endcoordinates', type=int, nargs=2, action="append")

    #parser.parse_args('-s x1 z2 -e x2 z2'.split())

    # TODO Implement single chunk and specific chunk range implementation
    #parser.add_argument('c', '--chunk', nargs=2, action="append")

    block_to_fix = parser.parse_args().fixblock

    start_x_z = tuple(parser.parse_args().startcoordinates[0])
    end_x_z = tuple(parser.parse_args().endcoordinates[0])
    coordinate_range = [start_x_z, end_x_z]

    #coordinate_range = [(5120, -512), (5616, -16)]

    main(block_to_fix, coordinate_range)