from os.path import join

from python_nbt.nbt import write_to_nbt_file, read_from_nbt_file

from . import settings


def remove_nodes(nbt_file, pos_long_list):
    for node in nbt_file["data"]["Nodes"]:
        if node["Pos"] in pos_long_list:
            print(f'Node located at {str(node["Pos"].value)} removed')
            del node

    return nbt_file


def get_longs(long_file):
    long_list = []
    for line in long_file:
        long_list.append(line.replace(' ', ''))
    return long_list


def get_and_remove_nodes(nbt_file, long_list):
    counter = 0
    for node in nbt_file["data"]["Nodes"]: 
        if long_list.count(str(node["Pos"].value)) == 1:
            del nbt_file["data"]["Nodes"][counter]
            print(f'Node located at {str(node["Pos"].value)} removed')
        counter += 1
    return nbt_file


def remove_nodes_1():
    """
    # Remove all nodes who are located at long POS
    """
    long_file = open(join(settings.DATA_PATH, 'longs.txt'))
    long_list = get_longs(long_file)
    
    nbt_file = read_from_nbt_file(join(settings.DATA_PATH, 'world/data/refinedstorage_nodes.dat'))
    nbt_json = nbt_file.json_obj(full_json=True)
    new_nbt_file = get_and_remove_nodes(nbt_file, long_list)
    write_to_nbt_file(join(settings.DATA_PATH, 'world/data/refinedstorage_nodes_NEW.dat'), new_nbt_file)