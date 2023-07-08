import os
import xml.etree.ElementTree as ElementTree


def get_list_priority(dir_name: str) -> list[(str, str, str), ...]:
    l_row_entrant_priority = []
    l_file = os.listdir(dir_name)
    _ = 0
    for f in l_file:
        path_file = f'{dir_name}/' + f
        root_node = ElementTree.parse(path_file).getroot()

        for row in root_node:
            l_row_entrant_req_com_id_and_ent_id_and_com_id = []
            row_entrant_req_com_id = str(row.get('reqComId'))
            if row_entrant_req_com_id != 'None':
                row_entrant_entrant_id = str(row.get('entrantId'))
                row_entrant_competition_id = str(row.get('competitionId'))
                l_row_entrant_req_com_id_and_ent_id_and_com_id.append((row_entrant_entrant_id,
                                                                       row_entrant_req_com_id,
                                                                       row_entrant_competition_id))
                if l_row_entrant_req_com_id_and_ent_id_and_com_id[0] in l_row_entrant_priority:
                    ...
                else:
                    l_row_entrant_priority.append((row_entrant_entrant_id,
                                                   row_entrant_req_com_id,
                                                   row_entrant_competition_id))
    return l_row_entrant_priority
