import os
import xml.etree.ElementTree as ET


def get_list_priority(dir_name: str) -> list:
    l_row_entrant_priority = []
    l_file = os.listdir(dir_name)
    for f in l_file:
        path_file = f'{dir_name}/' + f
        # print(path_file)
        root_node = ET.parse(path_file).getroot()

        for row in root_node:
            row_entrant_priority = row.get('reqComId')
            if row_entrant_priority is not None:
                # print(row_entrant_priority)
                l_row_entrant_priority.append(str(row_entrant_priority))

    # print(l_row_entrant_priority)
    return l_row_entrant_priority

