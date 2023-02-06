import json


def get_rs_nodes(nbt_file, node_type: str) -> list:
    """Get refined-storage nodes from nbt-file
    :param nbt_file: nbt-file object
    :param node_type: node-types (block-id) to check for, everything else is ignored
    """

    long_pos_list = []
    for node in nbt_file["data"]["Nodes"]:
        # data = node["Data"]
        position = node["Pos"]
        node_id = node["Id"]

        # we only care about importer and exporter
        if node_id != node_type:
            continue

        """ Implementation for cover-data not yet done
        # check for cover data
        if "Cover" in data.keys():
            if "value" in data["Cover"].keys():
                print(data["Cover"]["value"]
            else:
                print("Check if corrupt cover data?)

        """

        # replace ' with " in the id string, so json.loads can read it
        pos_json = json.loads(str(position).replace("\'", "\""))

        long_pos_list.append(pos_json["value"])

    return long_pos_list
