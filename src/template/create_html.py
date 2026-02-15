import logging
import os
import sys
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from pathlib import Path

from defusedxml.ElementTree import parse
from jinja2 import (
    Environment,
    FileSystemLoader,
)

from src.core.config import settings
from src.list_priority import (
    PriorityEntry,
    get_list_priority,
)


logger = logging.getLogger(__name__)


@dataclass
class Student:
    number: int | None = None
    snils: str | None = None
    total_points: str | None = None
    marks: list[str] | None = None
    total_points_id: str | None = None
    preference_category_title: str | None = None
    original_passed: str | None = None
    print_priority: str | None = None
    vip_priority: str | None = None
    accepted: str | None = None
    status: str | None = None


@dataclass
class ProgramInfo:
    faculty: str | None = None
    subject: str | None = None
    spec: str | None = None
    form: str | None = None
    compensation_type: str | None = None
    competition_type: str | None = None
    plan: str | None = None
    statement_count: int = 0
    colspan: int = 0
    short_titles: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Основные точки входа
# ---------------------------------------------------------------------------


def create_html(
    pk_name: str,
    file_xml_name: str,
    dir_name_for_priority: str,
) -> None:
    """
    Генерирует HTML-отчет по XML-файлу с абитуриентами.

    pk_name: тип приемной кампании (bak, mag, spo, asp)
    file_xml_name: имя XML-файла (без расширения)
    dir_name_for_priority: директория для поиска приоритетов
    """
    row_priority: list[PriorityEntry] = []
    if pk_name in ("bak", "mag"):
        row_priority = get_list_priority(directory=dir_name_for_priority)

    root_node = _parse_xml_file(f"{file_xml_name}.xml")
    enrollment = root_node.get("enrollmentCampaignTitle")
    current_date_time = _format_datetime(root_node.get("currentDateTime", ""))

    main_list: dict = {
        "pk_name": pk_name,
        "information": [],
        "students": [],
        "enrollment": enrollment,
        "current_date_time": current_date_time,
    }

    snils_in_separate_quota = _collect_separate_quota_snils(root_node, pk_name)

    for competition in root_node:
        for row_program in competition:
            info, students = _process_program(
                row_program,
                pk_name,
                row_priority,
                snils_in_separate_quota,
            )
            if info and students:
                main_list["information"].append(info)
                main_list["students"].append(students)

    template_dir = _resolve_template_dir()
    current_year = datetime.now().year
    output_filename = f"spiski_abitur_{pk_name}_{current_year}.html"
    _render_html(template_dir, main_list, output_filename)
    logger.info("HTML-отчет сгенерирован: %s", output_filename)


# ---------------------------------------------------------------------------
# Разбор XML
# ---------------------------------------------------------------------------


def _parse_xml_file(file_path: str):
    """Парсит XML-файл и возвращает корневой элемент."""
    root = parse(file_path, forbid_dtd=True).getroot()
    if root is None:
        raise ValueError(f"XML-файл не содержит корневого элемента: {file_path}")
    return root


def _format_datetime(raw: str) -> str:
    """Преобразует строку даты из XML формата в читаемый вид."""
    if len(raw) < 16:
        return raw
    return f"{raw[8:10]}.{raw[5:7]}.{raw[:4]}  {raw[11:16]}"


def _resolve_template_dir() -> str:
    """Определяет директорию шаблонов (PyInstaller или стандартная)."""
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return os.path.join(meipass, "template")
    return str(Path("src") / "template")


# ---------------------------------------------------------------------------
# Сбор СНИЛС из отдельной квоты
# ---------------------------------------------------------------------------


def _collect_separate_quota_snils(root_node, pk_name: str) -> list[str]:
    """Собирает список СНИЛС абитуриентов из конкурсов типа 'Отдельная квота'."""
    result: list[str] = []
    if pk_name not in ("bak", "mag"):
        return result

    for competition in root_node:
        for row_program in competition:
            competition_type = row_program.get("competitionType")
            if competition_type is None or str(competition_type) != "Отдельная квота":
                continue
            for sub_row in row_program:
                for entry in sub_row:
                    position = entry.get("position")
                    snils = entry.get("snils")
                    if position is not None and snils is not None and snils not in result:
                        result.append(snils)

    return result


# ---------------------------------------------------------------------------
# Обработка образовательной программы
# ---------------------------------------------------------------------------


def _process_program(
    row_program,
    pk_name: str,
    row_priority: list[PriorityEntry],
    snils_in_separate_quota: list[str],
) -> tuple[dict | None, dict | None]:
    """Обрабатывает одну образовательную программу и возвращает (info, students)."""
    meta = _extract_program_meta(row_program, pk_name)
    if meta is None:
        return None, None

    students_data = _StudentCollector(pk_name, row_priority, snils_in_separate_quota)

    for sub_row_program in row_program:
        for entry in sub_row_program:
            short_title = entry.get("shortTitle")
            if short_title is not None:
                students_data.short_titles.append(short_title)

            position = entry.get("position")
            if position is None:
                # Обработка программной специфики
                program_spec = entry.get("programSpec")
                if program_spec is not None:
                    meta["program_spec"] = program_spec
                colspan = _get_colspan(pk_name)
                if colspan:
                    meta["colspan"] = colspan
                continue

            students_data.process_entry(entry, sub_row_program, meta.get("edu_program_id", ""))

    return _build_result(meta, students_data, pk_name)


def _extract_program_meta(row_program, pk_name: str) -> dict | None:
    """Извлекает метаданные образовательной программы."""
    faculty = row_program.get("formativeOrgUnitTitle")

    if pk_name == "spo":
        edu_program_subject = row_program.get("programSetPrintTitle")
        edu_program_id = ""
    else:
        edu_program_subject = row_program.get("eduProgramSubject")
        edu_program_id = row_program.get("id", "")

    edu_program_form = row_program.get("eduProgramForm")
    compensation_type = row_program.get("compensationTypeShortTitle")
    competition_type_raw = row_program.get("competitionType")
    plan_recruitment = row_program.get("plan")

    competition_type_display = _format_competition_type(
        competition_type_raw,
        compensation_type,
        pk_name,
    )

    if plan_recruitment is not None:
        if compensation_type != "по договору" and pk_name != "spo":
            plan_recruitment = f"{plan_recruitment} за исключением квот"

    return {
        "faculty": faculty,
        "edu_program_subject": edu_program_subject,
        "edu_program_id": edu_program_id,
        "edu_program_form": edu_program_form,
        "compensation_type": compensation_type,
        "competition_type_raw": str(competition_type_raw) if competition_type_raw else "",
        "competition_type_display": competition_type_display,
        "plan_recruitment": plan_recruitment,
        "program_spec": None,
        "colspan": _get_colspan(pk_name),
    }


def _format_competition_type(
    competition_type: str | None,
    compensation_type: str | None,
    pk_name: str,
) -> str:
    """Форматирует тип конкурса для отображения."""
    if competition_type is None:
        return ""

    if compensation_type == "по договору":
        return ""

    s = str(competition_type)
    lowered = s[0].lower() + s[1:]

    if pk_name in ("bak", "mag"):
        return (
            f" - {lowered}<br> <H4>Зачисление на бюджет - в "
            "соответствии с высшим приоритетом, "
            "по которому поступающий проходит по "
            "конкурсу</H4>"
        )

    return f" - {lowered}"


def _get_colspan(pk_name: str) -> int:
    """Возвращает colspan для таблицы в зависимости от типа ПК."""
    return {"bak": 3, "mag": 1, "spo": 1, "asp": 2}.get(pk_name, 0)


# ---------------------------------------------------------------------------
# Сборщик данных студентов
# ---------------------------------------------------------------------------


class _StudentCollector:
    """Аккумулирует данные студентов при обработке XML-записей."""

    def __init__(
        self,
        pk_name: str,
        row_priority: list[PriorityEntry],
        snils_in_separate_quota: list[str],
    ) -> None:
        self.pk_name = pk_name
        self.row_priority = row_priority
        self.snils_in_separate_quota = snils_in_separate_quota

        self.short_titles: list[str] = []
        self.numbers: list[int] = []
        self.snils_list: list[str] = []
        self.total_points: list[str] = []
        self.marks: list[list[str]] = []
        self.total_points_id: list = []
        self.preference_titles: list[str] = []
        self.original_passed: list[str] = []
        self.print_priorities: list[str] = []
        self.vip_priorities: list[str] = []
        self.accepted: list[str] = []
        self.statuses: list[str] = []
        self.average_marks: list[str] = []
        self.statement_count: int = 0

    def process_entry(self, entry, sub_row_program, edu_program_id: str) -> None:
        """Обрабатывает одну запись абитуриента."""
        position = entry.get("position")
        if position is None:
            return

        for pos in position.split():
            self.numbers.append(int(pos))

        self._collect_preference(entry)
        self._collect_snils(entry)
        self._collect_accepted(entry)
        self._collect_status(entry)
        self._collect_total_points(entry)
        self._collect_marks(entry, sub_row_program)
        self._collect_original_passed(entry)
        self._collect_priority(entry)
        self._collect_vip_priority(entry, edu_program_id)

    def _collect_preference(self, entry) -> None:
        preference = entry.get("preferenceCategoryTitle")
        self.preference_titles.append("Да" if preference is not None else "Нет")

    def _collect_snils(self, entry) -> None:
        snils = entry.get("snils")
        competition_type_title = ""  # будет установлен из контекста
        number = None

        if (
            snils is None
            or competition_type_title == "Отдельная квота"
            or snils in self.snils_in_separate_quota
            or not settings.app.use_snils.get(self.pk_name, False)
        ):
            for personal_number in entry.findall("entrantPersonalNumber"):
                number = personal_number.text
                self.statement_count += 1
                self.snils_list.append(number)
        else:
            self.statement_count += 1
            self.snils_list.append(snils)

    def _collect_accepted(self, entry) -> None:
        accepted_raw = entry.get("acceptedEntrant")
        snils = entry.get("snils")
        number = None
        for pn in entry.findall("entrantPersonalNumber"):
            number = pn.text

        if accepted_raw is not None and (snils is not None or number is not None):
            self.accepted.append("Да" if accepted_raw == "true" else "Нет")

    def _collect_status(self, entry) -> None:
        status = entry.get("status")
        if status is not None:
            self.statuses.append(status)

    def _collect_total_points(self, entry) -> None:
        if self.pk_name == "spo":
            avg_mark = entry.get("averageEduInstitutionMark", "-")
            self.average_marks.append(avg_mark if avg_mark else "-")

        total_points = entry.get("finalMark")
        if total_points is not None:
            self.total_points.append(total_points)

    def _collect_marks(self, entry, sub_row_program) -> None:
        marks_raw = entry.get("marks")
        if marks_raw is not None:
            if self.pk_name == "spo" and marks_raw == "":
                marks_raw = "\u2014"
            self.marks.append(marks_raw.split())

        if self.pk_name == "asp":
            total_id = 0
            for mark_item in sub_row_program:
                achievements = mark_item.findall("markEntrantAchievements")
                for achievement in achievements:
                    total_id += int(achievement.text.split()[-1])
            self.total_points_id.append(total_id)
        else:
            achievement_mark = entry.get("achievementMark")
            if achievement_mark is not None:
                self.total_points_id.append(achievement_mark)

    def _collect_original_passed(self, entry) -> None:
        original = entry.get("originalIn")
        if original is not None:
            self.original_passed.append("Да" if original == "true" else "Нет")

    def _collect_priority(self, entry) -> None:
        priority = entry.get("printPriority")
        if priority is not None:
            self.print_priorities.append(priority)

    def _collect_vip_priority(self, entry, edu_program_id: str) -> None:
        if self.pk_name not in ("bak", "mag"):
            return

        entrant_id = entry.get("entrantId", "")
        req_comp_id = entry.get("reqCompId", "")
        vip = " "

        for priority_entry in self.row_priority:
            if (
                entrant_id == priority_entry[0]
                and req_comp_id == priority_entry[1]
                and edu_program_id == priority_entry[2]
            ):
                vip = "Да" if priority_entry[3] and not priority_entry[4] else ""
                break

        self.vip_priorities.append(vip)


# ---------------------------------------------------------------------------
# Формирование итогового результата
# ---------------------------------------------------------------------------


def _build_result(
    meta: dict,
    collector: _StudentCollector,
    pk_name: str,
) -> tuple[dict | None, dict | None]:
    """Собирает итоговые словари info и students из метаданных и коллектора."""
    faculty = meta["faculty"]
    edu_program_subject = meta["edu_program_subject"]
    program_spec = meta.get("program_spec")
    edu_program_form = meta["edu_program_form"]
    compensation_type = meta["compensation_type"]
    plan_recruitment = meta["plan_recruitment"]

    required_fields_present = (
        (faculty is not None or pk_name == "spo")
        and edu_program_subject is not None
        and (program_spec is not None or pk_name == "spo")
        and edu_program_form is not None
        and compensation_type is not None
        and plan_recruitment is not None
    )

    if not required_fields_present:
        return None, None

    info_list = {
        "faculty": [faculty],
        "edu_program_subject": [edu_program_subject],
        "program_spec": [program_spec],
        "edu_program_form": [edu_program_form, edu_program_form],
        "compensation_type_short_title": [compensation_type],
        "competition_type": [meta["competition_type_display"]],
        "plan_recruitment": [plan_recruitment],
        "statement": [collector.statement_count],
        "colspan": [meta["colspan"]],
        "short_title": [collector.short_titles],
    }

    student_data = {
        "number": collector.numbers,
        "snils": collector.snils_list,
        "total_points": collector.average_marks if pk_name == "spo" else collector.total_points,
        "marks": collector.marks,
        "total_points_id": collector.total_points_id,
        "preference_category_title": collector.preference_titles,
        "original_passed": collector.original_passed,
        "print_priority": collector.print_priorities,
        "vip_priority": collector.vip_priorities,
        "accepted": collector.accepted,
        "status": collector.statuses,
    }

    return info_list, student_data


# ---------------------------------------------------------------------------
# Рендеринг HTML
# ---------------------------------------------------------------------------


def _render_html(template_path: str, context: dict, output_path: str) -> None:
    """Генерирует HTML-файл из шаблона Jinja2."""
    env = Environment(
        loader=FileSystemLoader(template_path),
        autoescape=True,
    )
    template = env.get_template("template.html")
    html_content = template.render(context)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
