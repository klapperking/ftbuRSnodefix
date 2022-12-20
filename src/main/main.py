from python_nbt.nbt import read_from_nbt_file, NBTTagBase
import json
import test

"""
region_loc = "../../resources/FTBU_files/world/region"
region_file = "r.10.-1.mca"
"""


nodes_file_loc = "../../resources/FTBU_files/world/data/refinedstorage_nodes.dat"
file = read_from_nbt_file(nodes_file_loc)
# json_file = NBTTagBase.json_obj(file)

fix = ["refinedstorage:importer", "refined_storage:exporter"]

long_pos_list = []

for node in file["data"]["Nodes"]:
    data = node["Data"]
    position = node["Pos"]
    id = node["Id"]

    # we only care about importer and exporter
    if id not in fix:
        continue

    #replace ' with " in the id string, so json.loads can read it
    pos_json = json.loads(str(position).replace("\'", "\""))
    coordinates = test.main(int(pos_json["value"]))

    print(position, coordinates)
    long_pos_list.append(pos_json["value"])

#save to file
with open("pos_long_list.txt", "w") as out:
    for i in long_pos_list:
        out.write(str(i) + "\n")