import os
from typing import (
    List,
    Tuple,
)

from defusedxml.ElementTree import (
    parse,
    XMLParser,
)


def get_list_priority(dir_name: str) -> List[Tuple[str, str, str, bool, bool, bool]]:
    """
    Parse XML files in the given directory and return a list of tuples containing:
    (entrant_id, req_com_id, competition_id, is_budget, is_agree, is_priority_step).
    """
    priorities: List[Tuple[str, str, str, bool, bool, bool]] = []
    parser = XMLParser(
        forbid_dtd=True,
        forbid_entities=True,
        forbid_external=True,
    )

    for filename in os.listdir(dir_name):
        file_path = os.path.join(dir_name, filename)
        try:
            root = parse(file_path, parser=parser).getroot()
        except Exception:
            continue

        is_budget = root.get("isBudget") == "true"
        is_agree = root.get("isAgree") == "true"
        is_priority_step = root.get("isPriorityStep") == "true"

        for element in root:
            req_com_id = element.get("reqComId")
            if not req_com_id or req_com_id == "None":
                continue

            entrant_id = element.get("entrantId", "")
            competition_id = element.get("competitionId", "")
            entry = (
                entrant_id,
                req_com_id,
                competition_id,
                is_budget,
                is_agree,
                is_priority_step,
            )
            if entry not in priorities:
                priorities.append(entry)

    return priorities
