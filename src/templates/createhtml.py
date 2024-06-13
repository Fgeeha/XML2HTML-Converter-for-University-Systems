# src/templates/createhtml.py
import xml.etree.ElementTree as ElementTree
from utils import get_list_priority

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>{title}</title>
    <meta charset="UTF-8">
</head>
<body>
    <style>
        .enr-entrant-row-cutoff td {{ border-bottom: 6px solid #555; }}
    </style>
    <div class="container-fluid">
        <div class="row">
            <div class="col">
                <h1>{enrollment}<small class="text-muted"> по состоянию на {current_date_time}</small></h1>
                <hr>
                <div class="input-group mb-3">
                    <input type="text" class="form-control" placeholder="Поиск по СНИЛСу или персональному номеру" aria-label="Search">
                    <div class="input-group-append">
                        <button class="btn btn-outline-secondary" type="button">Поиск</button>
                    </div>
                </div>
                <hr>
                {faculty_section}
            </div>
        </div>
    </div>
</body>
</html>"""

FACULTY_SECTION_TEMPLATE = """<h5>{faculty}</h5>
<h2>{edu_program_subject}</h2>
<h3>{edu_program_form} форма обучения, {compensation_type_short_title}</h3>
<p>Заявлений — {statement}, число мест — {plan_recruitment}</p>
<div class="table-responsive">
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th rowspan="2">№</th>
                <th rowspan="2">СНИЛС или Личный номер</th>
                <th rowspan="2">Сумма баллов</th>
                {exam_headers}
            </tr>
            <tr>
                {exam_titles}
            </tr>
        </thead>
        <tbody>
            {entrant_rows}
        </tbody>
    </table>
</div>
<hr>"""

ENTRANT_ROW_TEMPLATE = """<tr class="{row_class}">
    <td>{number}</td>
    <td>{snils}</td>
    <td>{total_points}</td>
    {exam_results}
    <td>{total_points_id}</td>
    <td>{preference_category_title}</td>
    <td>{original_passed}</td>
    <td>{print_priority}</td>
    <td>{vip_priority}</td>
</tr>"""

def create_html(pk_name: str, file_xml_name: str, dir_name_for_priority: str) -> None:
    row_priority = get_list_priority(dir_name=dir_name_for_priority) if pk_name in ['bak', 'mag'] else []
    root_node = ElementTree.parse(f'{file_xml_name}.xml').getroot()
    enrollment = root_node.get('enrollmentCampaignTitle')
    current_date_time = str(root_node.get('currentDateTime'))
    current_date_time_r = f'{current_date_time[8:10]}.{current_date_time[5:7]}.{current_date_time[:4]} {current_date_time[11:16]}'
    faculty_sections = []

    for competition in root_node:
        for row_program in competition:
            faculty = row_program.get('formativeOrgUnitTitle')
            edu_program_subject = row_program.get('programSetPrintTitle') if pk_name == 'spo' else row_program.get('eduProgramSubject')
            edu_program_form = row_program.get('eduProgramForm')
            compensation_type_short_title = row_program.get('compensationTypeShortTitle')
            plan_recruitment = row_program.get('plan')
            statement = 0

            entrant_rows = []
            l_short_title = []
            for sub_row_program in row_program:
                for sub2_row_program in sub_row_program:
                    position = sub2_row_program.get('position')
                    snils = sub2_row_program.get('snils')
                    total_points = sub2_row_program.get('finalMark')
                    total_points_id = sub2_row_program.get('achievementMark')
                    preference_category_title = 'Да' if sub2_row_program.get('preferenceCategoryTitle') else 'Нет'
                    original_passed = 'Да' if sub2_row_program.get('originalIn') == 'true' else 'Нет'
                    print_priority = sub2_row_program.get('printPriority')
                    vip_priority = 'Да' if sub2_row_program.get('acceptedEntrant') == 'true' else ' '

                    short_title = sub2_row_program.get('title')
                    if short_title:
                        l_short_title.append(short_title)

                    row_class = 'table-success' if original_passed == 'Да' and vip_priority == 'Да' else ''
                    exam_results = ''.join([f'<td>{mark}</td>' for mark in sub2_row_program.get('marks', '').split() if mark])

                    if position:
                        entrant_rows.append(ENTRANT_ROW_TEMPLATE.format(
                            row_class=row_class,
                            number=position,
                            snils=snils,
                            total_points=total_points,
                            exam_results=exam_results,
                            total_points_id=total_points_id,
                            preference_category_title=preference_category_title,
                            original_passed=original_passed,
                            print_priority=print_priority,
                            vip_priority=vip_priority
                        ))

            if faculty and edu_program_subject and edu_program_form and compensation_type_short_title and plan_recruitment and entrant_rows:
                exam_headers = '<th colspan="{}">Результаты ВИ</th>'.format(len(l_short_title)) if l_short_title else ''
                exam_titles = ''.join([f'<th>{title}</th>' for title in l_short_title])

                faculty_sections.append(FACULTY_SECTION_TEMPLATE.format(
                    faculty=faculty,
                    edu_program_subject=edu_program_subject,
                    edu_program_form=edu_program_form,
                    compensation_type_short_title=compensation_type_short_title,
                    statement=statement,
                    plan_recruitment=plan_recruitment,
                    exam_headers=exam_headers,
                    exam_titles=exam_titles,
                    entrant_rows=''.join(entrant_rows)
                ))

    with open(f'spiski_{pk_name}_2024.html', 'w') as file_html:
        file_html.write(HTML_TEMPLATE.format(
            title=enrollment,
            enrollment=enrollment,
            current_date_time=current_date_time_r,
            faculty_section=''.join(faculty_sections)
        ))
