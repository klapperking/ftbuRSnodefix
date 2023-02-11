import json

from . import darkere_coord_from_int as darkere

def get_rs_nodes(nbt_file, coord_range: list) -> dict:
    """Get refined-storage nodes from nbt-file
    :param nbt_file: nbt-file object
    :param coord_range: Coordinate range from which to take nodes
    :param node_types: node-types (block-id) to check for, everything else is ignored
    """

    pos_dict = {}
    for node in nbt_file["data"]["Nodes"]:
        # data = node["Data"]
        position = node["Pos"]
        node_id = node["Id"]

        # convert longs to x,y,z coordinates
        x, y, z = darkere.from_long(position.value)

        # if block is outside coordinate range we ignore
        if x < coord_range[0][0] or x > coord_range[1][0]:
            continue
        if z < coord_range[0][1] or z > coord_range[1][1]:
            continue

        # create a dict with node_id: [pos, pos]
        if node_id.value not in pos_dict.keys():
            pos_dict[node_id.value] = [(x, y, z)]
        else:
            pos_dict[node_id.value].append((x, y, z))

    return pos_dict

