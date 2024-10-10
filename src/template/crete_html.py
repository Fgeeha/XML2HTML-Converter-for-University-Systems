import os
import sys

from defusedxml.ElementTree import parse
from jinja2 import (
    Environment,
    FileSystemLoader,
)

from src.list_priority import get_list_priority


def create_html(pk_name: str, file_xml_name: str, dir_name_for_priority: str) -> None:
    row_priority = []  # Создаем список записей в которых есть высший приоритет
    if pk_name in ("bak", "mag"):
        row_priority = get_list_priority(
            dir_name=dir_name_for_priority,
        )

    root_node = parse(
        f"{file_xml_name}.xml",
        forbid_dtd=True,
    ).getroot()
    enrollment = root_node.get("enrollmentCampaignTitle")
    current_date_time = str(root_node.get("currentDateTime"))
    current_date_time = (
        f"{current_date_time[8:10]}."
        f"{current_date_time[5:7]}.{current_date_time[:4]}  {current_date_time[11:16]}"
    )
    main_list = {
        "pk_name": pk_name,
        "information": [],
        "students": [],
        "enrollment": enrollment,
        "current_date_time": current_date_time,
    }

    l_snils_in_another_competition = []
    if pk_name in ("bak", "mag"):
        for competition in root_node:
            for row_program in competition:
                s_competition_type_title = ""
                competition_type = row_program.get("competitionType")
                if competition_type is not None:
                    s_competition_type_title = str(competition_type)
                for sub_row_program in row_program:
                    for sub2_row_program in sub_row_program:
                        position = sub2_row_program.get("position")
                        snils = sub2_row_program.get("snils")
                        if position is not None:
                            if s_competition_type_title == "Отдельная квота":
                                if snils not in l_snils_in_another_competition:
                                    l_snils_in_another_competition.append(snils)
    for competition in root_node:
        for row_program in competition:
            # Инициируем переменных
            s_compensation_type_short_title = ""
            average_edu_institution_mark = ""
            s_competition_type = ""
            s_competition_type_title = ""
            edu_program_subject = ""
            edu_program_id = ""
            faculty = row_program.get("formativeOrgUnitTitle")
            if pk_name == "spo":
                edu_program_subject = row_program.get("programSetPrintTitle")
            else:
                edu_program_subject = row_program.get("eduProgramSubject")
                edu_program_id = row_program.get("id")
            edu_program_form = row_program.get("eduProgramForm")
            compensation_type_short_title = row_program.get(
                "compensationTypeShortTitle",
            )
            if compensation_type_short_title is not None:
                s_compensation_type_short_title = str(compensation_type_short_title)
            competition_type = row_program.get("competitionType")
            if competition_type is not None:
                s_competition_type_title = str(competition_type)
                if s_compensation_type_short_title == "по договору":
                    s_competition_type = ""
                else:
                    s = str(competition_type)
                    if pk_name in ("bak", "mag"):
                        s_competition_type = (
                            " - "
                            + s[0].lower()
                            + s[1:]
                            + "<br> <H4>Зачисление на бюджет - в "
                            "соответствии с высшим приоритетом, "
                            "по которому поступающий проходит по "
                            "конкурсу</H4>"
                        )
                    else:
                        s_competition_type = f" - {s[0].lower() + s[1:]}"
            plan_recruitment = row_program.get("plan")
            if plan_recruitment is not None:
                if s_compensation_type_short_title == "по договору":
                    plan_recruitment = str(plan_recruitment)
                else:
                    if pk_name == "spo":
                        plan_recruitment = str(plan_recruitment)
                    else:
                        plan_recruitment = (
                            str(plan_recruitment) + " за исключением квот"
                        )
            # Инициируем начальные данные по каждому абитуриенту в каждой образовательной программе
            l_row_entrant_req_com_id_and_ent_id_and_com_id = []  # массив для проверки
            statement = 0  # Количество заявлений
            l_short_title = []  # Вступительные испытания
            l_number = []  # Номер заявлений по порядку
            l_snils = []  # СНИЛС
            l_entrant_id = []  # id
            l_total_points = []  # Сумма баллов
            l_preference_category_title = []  # Преимущественное право зачисления
            l_marks = []  # Результаты ВИ
            l_total_points_id = []  # Сумма баллов за индивидуальные достижения
            l_original_passed = []  # Сдан оригинал:да/нет
            l_status = []  # Статус
            l_print_priority = []  # Приоритет
            l_req_comp_id_highest_priority = []  # Нужно для Высший приоритет
            l_benefit_special_category_title = []  # Отдельная квота
            l_l_accepted = []  # list Согласие на зачисление
            average_edu_institution_mark_list = []  # СПО Средний балл по аттестат
            l_vip_priority = []  # Высший приоритет (Да/' ')

            for sub_row_program in row_program:
                for sub2_row_program in sub_row_program:
                    colspan = 0
                    if pk_name == "bak":
                        colspan = 3
                    elif pk_name in ("mag", "spo"):
                        colspan = 1
                    elif pk_name == "asp":
                        colspan = 2
                    program_spec = sub2_row_program.get("programSpec")
                    short_title = sub2_row_program.get("shortTitle")
                    if short_title is not None:
                        l_short_title.append(short_title)
                    position = sub2_row_program.get("position")  # Номер по порядку
                    if position is not None:
                        [
                            l_number.append(int(x)) for x in position.split()
                        ]  # Приоритет при поступлении
                        preference_category_title = sub2_row_program.get(
                            "preferenceCategoryTitle",
                        )
                        benefit_special_category_title = sub2_row_program.get(
                            "benefitSpecialCategoryTitle",
                        )
                        if preference_category_title is not None:
                            l_preference_category_title.append("Да")
                        else:
                            l_preference_category_title.append("Нет")
                        if benefit_special_category_title is not None:
                            l_benefit_special_category_title.append(
                                benefit_special_category_title,
                            )
                        else:
                            l_benefit_special_category_title.append("-")
                        # Находим ID каждой записи в таблице, для сверки и выставления высшего приоритета

                        number = None
                        snils = sub2_row_program.get("snils")
                        entrant_id = sub2_row_program.get(
                            "entrantId",
                        )  # Снилс ИЛИ Номер
                        if position is not None:
                            if (
                                snils is None
                                or s_competition_type_title == "Отдельная квота"
                                or snils in l_snils_in_another_competition
                            ):
                                for PersonalNumber in sub2_row_program.findall(
                                    "entrantPersonalNumber",
                                ):
                                    number = PersonalNumber.text
                                    statement += 1
                                    l_snils.append(number)
                            else:
                                statement += 1
                                l_snils.append(snils)
                            l_entrant_id.append(entrant_id)
                            if sub2_row_program.get("acceptedEntrant") is not None and (
                                sub2_row_program.get("snils") is not None
                                or number is not None
                            ):
                                l_accepted = sub2_row_program.get(
                                    "acceptedEntrant",
                                )  # Согласие на зачисление

                                if l_accepted == "true":
                                    l_l_accepted.append("Да")
                                elif l_accepted == "false" or l_accepted is None:
                                    l_l_accepted.append("Нет")

                            req_comp_id_highest_priority = sub2_row_program.get(
                                "reqCompId",
                            )
                            if req_comp_id_highest_priority is not None:
                                l_req_comp_id_highest_priority.append(
                                    str(req_comp_id_highest_priority),
                                )

                            status = sub2_row_program.get("status")
                            if status is not None:
                                l_status.append(status)

                            if pk_name == "spo":
                                average_edu_institution_mark = sub2_row_program.get(
                                    "averageEduInstitutionMark",
                                )  # Средний балл по аттестату
                                if average_edu_institution_mark is None:
                                    average_edu_institution_mark = "-"
                                average_edu_institution_mark_list.append(
                                    average_edu_institution_mark,
                                )

                            total_points = sub2_row_program.get(
                                "finalMark",
                            )  # Сумма баллов
                            if total_points is not None:
                                l_total_points.append(total_points)
                                if (
                                    pk_name == "spo"
                                    and status == "Сданы ВИ"
                                    and total_points != "—"
                                ):
                                    if total_points == "—":
                                        average_edu_institution_mark = (
                                            average_edu_institution_mark.split()
                                        )
                                        l_total_points.append(
                                            average_edu_institution_mark,
                                        )

                            marks = sub2_row_program.get(
                                "marks",
                            )  # Результаты сдачи вступительных испытаний (по 3 сразу)
                            if marks is not None:
                                if pk_name == "spo":
                                    if marks == "":
                                        marks = "—"
                                s = marks.split()
                                l_marks.append(s)
                            if pk_name == "asp":
                                total_points_id = 0
                                for mark_entrant_achievements in sub_row_program:
                                    achievements = mark_entrant_achievements.findall(
                                        "markEntrantAchievements",
                                    )

                                    if achievements:
                                        for achievement in achievements:
                                            achievement_list = int(
                                                achievement.text.split(" ")[-1],
                                            )
                                            total_points_id += achievement_list
                                        # на выходе total_points_id
                            else:
                                total_points_id = sub2_row_program.get(
                                    "achievementMark",
                                )  # Сумма баллов за индивидуальные достижения
                            if total_points_id is not None:
                                l_total_points_id.append(total_points_id)

                            original_passed = sub2_row_program.get(
                                "originalIn",
                            )  # Сдан оригинал:да/нет
                            if original_passed is not None:
                                if original_passed == "false":
                                    l_original_passed.append("Нет")
                                if original_passed == "true":
                                    l_original_passed.append("Да")

                            print_priority = sub2_row_program.get(
                                "printPriority",
                            )  # Приоритет
                            if print_priority is not None:
                                l_print_priority.append(print_priority)
                            l_row_entrant_req_com_id_and_ent_id_and_com_id.append(
                                (
                                    entrant_id,
                                    req_comp_id_highest_priority,
                                    edu_program_id,
                                ),
                            )
                            if pk_name in ("bak", "mag"):
                                vip_priority = " "
                                for list_row_priority in row_priority:
                                    if (
                                        entrant_id == list_row_priority[0]
                                        and req_comp_id_highest_priority
                                        == list_row_priority[1]
                                        and edu_program_id == list_row_priority[2]
                                    ):
                                        if (
                                            list_row_priority[3]
                                            and not list_row_priority[4]
                                        ):
                                            vip_priority = "Да"
                                        else:
                                            vip_priority = ""
                                l_vip_priority.append(vip_priority)

            if (
                (faculty is not None or pk_name == "spo")
                and (edu_program_subject is not None)
                and (program_spec is not None or pk_name == "spo")
                and (edu_program_form is not None)
                and (compensation_type_short_title is not None)
                and (edu_program_form is not None)
                and (plan_recruitment is not None)
            ):
                info_list = {
                    "faculty": [],
                    "edu_program_subject": [],
                    "program_spec": [],
                    "edu_program_form": [],
                    "compensation_type_short_title": [],
                    "competition_type": [],
                    "plan_recruitment": [],
                    "statement": [],
                    "colspan": [],
                    "short_title": [],
                }

                info_list["faculty"].append(faculty)
                info_list["edu_program_subject"].append(edu_program_subject)
                info_list["program_spec"].append(program_spec)
                info_list["edu_program_form"].append(edu_program_form)
                info_list["compensation_type_short_title"].append(
                    compensation_type_short_title,
                )
                info_list["edu_program_form"].append(edu_program_form)
                info_list["plan_recruitment"].append(plan_recruitment)
                info_list["statement"].append(statement)
                info_list["colspan"].append(colspan)
                info_list["short_title"].append(l_short_title)
                info_list["competition_type"].append(s_competition_type)

                student_data = {
                    "number": l_number,  # Number
                    "snils": l_snils,  # СНИЛС или Личный номер
                    "total_points": (
                        average_edu_institution_mark_list
                        if pk_name == "spo"
                        else l_total_points
                    ),  # Сумма баллов
                    "marks": l_marks,  # Результаты ВИ
                    "total_points_id": l_total_points_id,  # Сумма баллов за ИД
                    "preference_category_title": l_preference_category_title,  # Преимущественное право зачисления
                    "original_passed": l_original_passed,  # Сдан оригинал (отметка на ЕПГУ)
                    "print_priority": l_print_priority,  # Приоритет
                    "vip_priority": l_vip_priority,  # Высший приоритет (Да/' ')
                    "accepted": l_l_accepted,  # Согласие на зачисление
                    "status": l_status,  # Статус
                }
                main_list["information"].append(info_list)
                main_list["students"].append(student_data)

    # Настройка Jinja2
    # Определяем путь к директории с шаблонами
    if hasattr(sys, "_MEIPASS"):
        # Путь для PyInstaller
        template_dir = os.path.join(sys._MEIPASS, "template")
    else:
        # Путь для разработки
        template_dir = "src/template/"

    # Создаем Jinja2 Environment
    env = Environment(loader=FileSystemLoader(template_dir))

    # Загружаем шаблон
    template = env.get_template("template.html")

    # Генерация HTML из шаблона, используя render
    html_content = template.render(main_list)

    # Запись результата в файл
    with open(f"spiski_abitur_{pk_name}_2024.html", "w", encoding="utf-8") as file_html:
        file_html.write(html_content)
