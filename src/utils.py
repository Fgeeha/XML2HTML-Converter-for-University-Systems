
# src/utils.py
import os
import xml.etree.ElementTree as ElementTree

def check_dir(dir_name: str) -> None:
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def get_list_priority(dir_name: str) -> list:
    l_row_entrant_priority = []
    l_file = os.listdir(dir_name)
    for f in l_file:
        path_file = f'{dir_name}/{f}'
        root_node = ElementTree.parse(path_file).getroot()
        is_budget = root_node.get('isBudget') == 'true'
        is_agree = root_node.get('isAgree') == 'true'
        for row in root_node:
            row_entrant_req_com_id = row.get('reqComId')
            if row_entrant_req_com_id != 'None':
                row_entrant_entrant_id = row.get('entrantId')
                row_entrant_competition_id = row.get('competitionId')
                l_row_entrant_priority.append((row_entrant_entrant_id, row_entrant_req_com_id, row_entrant_competition_id, is_budget, is_agree))
    return l_row_entrant_priority