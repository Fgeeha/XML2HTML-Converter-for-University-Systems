import os

from defusedxml.ElementTree import parse


def parse_file_for_priority(path_file: str) -> list:
    root_node = parse(
        path_file,
        forbid_dtd=True,
    ).getroot()
    is_budget = (
        root_node.get("isBudget") == "true"
    )  # Если бюджет True, если платное False.
    is_agree = (
        root_node.get("isAgree") == "true"
    )  # Если по согласию (поданные оригиналы) True, если поданным конкурсам False.

    is_priority_step = (
        root_node.get("isPriorityStep") == "true"
    )  # Если приоритетный этап True, иначе False Закомитить после приоритетного этапа

    l_row_entrant_priority = []
    for row in root_node:
        l_row_entrant_req_com_id_and_ent_id_and_com_id = []
        row_entrant_req_com_id = str(row.get("reqComId"))
        if row_entrant_req_com_id != "None":
            row_entrant_entrant_id = str(row.get("entrantId"))
            row_entrant_competition_id = str(row.get("competitionId"))
            l_row_entrant_req_com_id_and_ent_id_and_com_id.append(
                (
                    row_entrant_entrant_id,
                    row_entrant_req_com_id,
                    row_entrant_competition_id,
                ),
            )
            if (
                l_row_entrant_req_com_id_and_ent_id_and_com_id[0]
                in l_row_entrant_priority
            ):
                ...
            else:
                l_row_entrant_priority.append(
                    (
                        row_entrant_entrant_id,
                        row_entrant_req_com_id,
                        row_entrant_competition_id,
                        is_budget,
                        is_agree,
                        is_priority_step,
                    ),
                )
    return l_row_entrant_priority


def get_list_priority(dir_name: str) -> list[(str, str, str, bool, bool)]:
    l_row_entrant_priority = []
    l_file = os.listdir(dir_name)
    for f in l_file:
        path_file = f"{dir_name}/{f}"
        l_row_entrant_priority.extend(parse_file_for_priority(path_file))
    return l_row_entrant_priority
