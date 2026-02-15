import logging
from pathlib import Path

from defusedxml.ElementTree import (
    XMLParser,
    parse,
)


logger = logging.getLogger(__name__)

PriorityEntry = tuple[str, str, str, bool, bool, bool]
"""(entrant_id, req_com_id, competition_id, is_budget, is_agree, is_priority_step)"""


def get_list_priority(directory: str | Path) -> list[PriorityEntry]:
    """
    Парсит XML-файлы в указанной директории и возвращает список кортежей:
    (entrant_id, req_com_id, competition_id, is_budget, is_agree, is_priority_step).
    """
    seen: set[PriorityEntry] = set()
    priorities: list[PriorityEntry] = []
    parser = XMLParser(
        forbid_dtd=True,
        forbid_entities=True,
        forbid_external=True,
    )

    dir_path = Path(directory)
    for file_path in dir_path.iterdir():
        if not file_path.is_file():
            continue
        try:
            root = parse(str(file_path), parser=parser).getroot()
        except Exception:
            logger.warning("Не удалось распарсить файл приоритетов: %s", file_path.name)
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
            entry: PriorityEntry = (
                entrant_id,
                req_com_id,
                competition_id,
                is_budget,
                is_agree,
                is_priority_step,
            )
            if entry not in seen:
                seen.add(entry)
                priorities.append(entry)

    return priorities
