import os
from typing import List, Tuple
from defusedxml.ElementTree import parse, ParseError


def get_priority_list(directory: str) -> List[Tuple[str, str, str, bool, bool]]:
    """
    Parse all XML files in the given directory and extract entries with priority info.

    Returns a list of tuples:
      (entrant_id, request_competition_id, competition_id, is_budget, is_agree)
    """
    priority_entries: List[Tuple[str, str, str, bool, bool]] = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            tree = parse(filepath)
            root = tree.getroot()
        except (ParseError, FileNotFoundError) as e:
            continue

        is_budget = root.get("isBudget", "false").lower() == "true"
        is_agree = root.get("isAgree", "false").lower() == "true"

        for child in root:
            req_com_id = child.get("reqComId")
            if not req_com_id or req_com_id == "None":
                continue

            entrant_id = child.get("entrantId", "")
            competition_id = child.get("competitionId", "")
            entry = (entrant_id, req_com_id, competition_id, is_budget, is_agree)

            if entry not in priority_entries:
                priority_entries.append(entry)

    return priority_entries


if __name__ == "__main__":
    directory_path = "path/to/xml/files"
    priorities = get_priority_list(directory_path)
    for p in priorities:
        print(p)
