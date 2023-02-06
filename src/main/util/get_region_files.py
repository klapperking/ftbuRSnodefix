


def coordinates_to_region_naming(coordinate_range: list) -> list:
    """
    Get region-file-name pieces to use for string-stitching
    e.g [(9, -2), (10, 0)]
    :param coordinate_range: X,Z coordinates to look for
    """

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

        if not tuple(new_coord_pair) in region_naming_range:
            region_naming_range.append(tuple(new_coord_pair))

    return region_naming_range


def get_region_names(region_naming_range: list) -> list:
    """
    Get all region-filename-numbers for a coordinate-range
    :param region_naming_range:
    :return: List of all region-file-name-string-pieces
    """

    start_region = region_naming_range[0]
    end_region = region_naming_range[1]

    # shortcoming - If the end borders of the coordinate range are exactly at chunk-change/region-change coordinates,
    # we will check unnecessary regions as well

    region_file_names = []
    for x in range(start_region[0], end_region[0] + 1):
        for y in range(start_region[1], end_region[1] + 1):

            region_name_numbers = (x, y)
            region_file_names.append(region_name_numbers)

    return region_file_names
