import xml.etree.ElementTree as ET
from spisokpriority import get_list_priority


def create_html(pk_name: str,
                file_xml_name: str,
                dir_name_for_priority: str
                ) -> None:

    # Создаем список записей в которых есть высший приоритет
    row_priority = []
    if pk_name == 'bak' or pk_name == 'mag':
        row_priority = get_list_priority(dir_name=dir_name_for_priority)
    # Имя и путь к HTML файлу
    file_html_name = f'list_on_the_website_{pk_name}_2023.html'
    file_html = open(file_html_name, 'w')
    # Формируем заголовок html файла
    file_html.write('<html>\n')
    file_html.write('   <head>\n')
    file_html.write('      <link '
                    'href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" '
                    'rel="stylesheet" '
                    'integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" '
                    'crossorigin="anonymous">\n')
    file_html.write('   </head>\n')
    # Формируем тело html файла
    file_html.write('   <body>\n')
    file_html.write('      <style '
                    'type="text/css">.enr-entrant-row-cutoff td { border-bottom: 6px solid #555; }'
                    '</style>\n')
    file_html.write('      <div class="container-fluid">\n')
    file_html.write('         <div class="row">\n')
    file_html.write('            <div class="col">\n')
    # Парсим XML файл с именем sample.xml
    root_node = ET.parse(f'{file_xml_name}.xml').getroot()
    # Получаем данные для заголовка страницы и записываем их в html файл
    enrollment = root_node.get('enrollmentCampaignTitle')
    current_date_time = str(root_node.get('currentDateTime'))
    # формируем время по образцу: по состоянию на 16.05.2023 10:30
    current_date_time_r = f'{current_date_time[8:10]}.' \
                          f'{current_date_time[5:7]}.{current_date_time[:4]}  {current_date_time[11:16]}'
    file_html.write(f'               <h1>{enrollment}<small class="text-muted"> '
                    f'по состоянию на {current_date_time_r}</small></h1>\n')
    file_html.write('               <hr>\n')
    # Парсим на два уровня вниз. Здесь нам нужны образовательные программы
    for competition in root_node:
        for row_program in competition:
            # Инициируем переменных
            s_compensation_type_short_title = ''
            average_edu_institution_mark = ''
            s_faculty = ''
            s_edu_program_form = ''
            s_plan_recruitment = ''
            s_competition_type = ''
            # Формируем заголовок каждой образовательной программы с названием факультета,
            # название программы, профилем и пр.
            # Факультет
            faculty = row_program.get('formativeOrgUnitTitle')
            if faculty is not None:
                s_faculty = str(faculty)
            # Уровень образование
            edu_level = row_program.get('eduLevel')
            if edu_level is not None:
                s_edu_level = str(edu_level)
            # На базе какой программы/уровня поступают абитуриенты
            edu_level_requirement_genetive = row_program.get('eduLevelRequirementGenetiveTitle')
            if edu_level_requirement_genetive is not None:
                s_edu_level_requirement_genetive = str(edu_level_requirement_genetive)
            # Направление
            edu_program_subject = row_program.get('eduProgramSubject')
            if edu_program_subject is not None:
                ...
                # print(edu_program_subject)
            # Форма обучения
            edu_program_form = row_program.get('eduProgramForm')
            if edu_program_form is not None:
                s_edu_program_form = str(edu_program_form)
                # print(eduProgramForm)
            # Договор/бюджет
            compensation_type_short_title = row_program.get('compensationTypeShortTitle')
            if compensation_type_short_title is not None:
                s_compensation_type_short_title = str(compensation_type_short_title)
                # print(compensation_type_short_title)
            # условия поступления
            competition_type = row_program.get('competitionType')
            if competition_type is not None:
                if s_compensation_type_short_title == 'по договору':
                    s_competition_type = ''
                else:
                    s = str(competition_type)
                    if pk_name == 'bak' or pk_name == 'mag':
                        s_competition_type = ' - ' + s[0].lower() + s[1:] + '<br> <H4>Зачисление на бюджет - в ' \
                                                                            'соответсвии с высшим приоритетом, ' \
                                                                            'по которому поступающий проходит по ' \
                                                                            'конкурсу</H4>'
                    else:
                        s_competition_type = f' - {s[0].lower() + s[1:]}'
                    """соответствии с высшим приоритетом"""
                    """Зачисление на бюджет - в соответствии с высшим 
                    приоритетом, по которому поступающий проходит по конкурсу"""
            # Число планируемых мест
            plan_recruitment = row_program.get('plan')
            if plan_recruitment is not None:
                if s_compensation_type_short_title == 'по договору':
                    s_plan_recruitment = str(plan_recruitment)
                else:
                    s_plan_recruitment = str(plan_recruitment) + ' за исключением других квот'
                # print(s_plan_recruitment)

            # Инициируем начальные данные по каждому абитуриенту в каждой образовательной программе
            s_program_spec = ''
            statement = 0
            l_short_title = []
            l_number = []
            l_snils = []
            l_total_points = []
            l_preference_category_title = []
            l_marks = []
            l_total_points_id = []
            l_original_passed = []
            l_status = []
            l_print_priority = []
            l_req_comp_id_highest_priority = []
            l_l_accepted = []
            """list Согласие на зачисление"""
            average_edu_institution_mark_list = []

            # Опускаемся на два уровня до данных по каждому абитуриенту
            for sub_row_program in row_program:
                # print(f'{sub_row_program = }')
                for sub2_row_program in sub_row_program:
                    # Данные по профилю
                    program_spec = sub2_row_program.get('programSpec')
                    if program_spec is not None:
                        s_program_spec = str(program_spec)
                        # print(s_program_spec)

                    # Перечень вступительных экзаменов по каждому направлению
                    short_title = sub2_row_program.get('shortTitle')
                    if short_title is not None:
                        l_short_title.append(short_title)

                    # Собираем данные для таблицы по каждому абитуриенту на каждой программе

                    number = None
                    snils = sub2_row_program.get('snils')
                    """Снилс ИЛИ Номер"""
                    if snils is not None:
                        statement += 1
                        l_snils.append(snils)
                    else:
                        for PersonalNumber in sub2_row_program.findall('entrantPersonalNumber'):
                            number = PersonalNumber.text
                            statement += 1
                            l_snils.append(number)
                    if sub2_row_program.get('acceptedEntrant') is not None \
                            and (sub2_row_program.get('snils') is not None or number is not None):

                        l_accepted = sub2_row_program.get('acceptedEntrant')
                        """Согласие на зачисление"""
                        if l_accepted == 'true':
                            l_l_accepted.append('да')
                        elif l_accepted == 'false' or l_accepted is None:
                            l_l_accepted.append('нет')

                    position = sub2_row_program.get('position')
                    """Номер по порядку"""
                    if position is not None:
                        l_number.append(position)
                        # Приоритет при поступлении
                        preference_category_title = sub2_row_program.get('preferenceCategoryTitle')
                        if preference_category_title is not None:
                            l_preference_category_title.append(preference_category_title)
                        else:
                            l_preference_category_title.append('нет')
                    # Находим ID каждой записи в таблице, для сверки и выставления высшего приоритета
                    req_comp_id_highest_priority = sub2_row_program.get('reqCompId')
                    if req_comp_id_highest_priority is not None:
                        l_req_comp_id_highest_priority.append(str(req_comp_id_highest_priority))
                        # print(str(req_comp_id_highest_priority))
                        # Статус
                    status = sub2_row_program.get('status')
                    if status is not None:
                        l_status.append(status)
                    if pk_name == 'spo':
                        """Средний балл по аттестату"""
                        average_edu_institution_mark = sub2_row_program.get('averageEduInstitutionMark')
                        if average_edu_institution_mark is None:
                            average_edu_institution_mark = '-'
                        average_edu_institution_mark_list.append(average_edu_institution_mark)

                    total_points = sub2_row_program.get('finalMark')
                    """Сумма баллов"""
                    if total_points is not None:
                        l_total_points.append(total_points)
                        if pk_name == 'spo' and status == 'Сданы ВИ' and total_points != '—':
                            if total_points == '—':
                                average_edu_institution_mark = average_edu_institution_mark.split()
                                l_total_points.append(average_edu_institution_mark)
                    # Результаты сдачи вступительных испытаний (по трем сразу)
                    marks = sub2_row_program.get('marks')
                    if marks is not None:
                        if pk_name == 'spo':
                            if marks == '':
                                marks = '—'
                        s = marks.split()
                        l_marks.append(s)

                    # Сумма баллов за индивидуальные достижения
                    total_points_id = sub2_row_program.get('achievementMark')
                    if total_points_id is not None:
                        l_total_points_id.append(total_points_id)
                    # Сдан оригинал:да/нет
                    original_passed = sub2_row_program.get('originalIn')
                    if original_passed is not None:
                        if original_passed == 'false':
                            l_original_passed.append('нет')
                        if original_passed == 'true':
                            l_original_passed.append('да')

                    # Приоритет
                    print_priority = sub2_row_program.get('printPriority')
                    if print_priority is not None:
                        l_print_priority.append(print_priority)
            # формируем по каждой образовательной программе информацию
            if faculty is not None:
                file_html.write(f'                  <h5>{s_faculty}</h5>\n')
            # if (edu_level is not None) and (edu_level_requirement_genetive is not None):
            #     file_html.write('                  <h4>'
            #                     + s_edu_level + ', на базе ' + s_edu_level_requirement_genetive.lower() + '</h4>\n')
            if edu_program_subject is not None:
                file_html.write(f'                  <h2>{str(edu_program_subject)} ({s_program_spec})</h2>\n')
            if (edu_program_form is not None) and (compensation_type_short_title is not None):
                file_html.write(f'                  <h3>{s_edu_program_form} форма обучения, '
                                f'{s_compensation_type_short_title + s_competition_type} </h3>\n')
            # Если есть заявления, то формируем таблицу со списком абитуриентов
            if statement > 0:
                # Заголовок таблицы
                file_html.write('                  <div class="table-responsive">\n')
                file_html.write('                     <table class="table table-bordered table-striped table-hover">\n')
                file_html.write('                       <thead>\n')
                file_html.write('                         <tr>\n')
                file_html.write('                           <th rowspan="2">№</th>\n')
                file_html.write('                           <th rowspan="2">СНИЛС или Личный номер</th>\n')
                file_html.write('                           <th rowspan="2">Сумма баллов</th>\n')
                if pk_name == 'bak' or pk_name == 'mag':
                    if pk_name == 'bak':
                        colspan = 3
                    elif pk_name == 'mag':
                        colspan = 1
                    file_html.write(f'                           <th colspan="{colspan}">Результаты ВИ</th>\n')
                    file_html.write('                           <th rowspan="2">Сумма баллов за ИД</th>\n')
                    file_html.write('                           <th rowspan="2">Основание приема без ВИ</th>\n')
                    file_html.write('                           <th rowspan="2">'
                                    'Преимущественное право зачисления</th>\n')
                    file_html.write('                           <th rowspan="2">Сдан оригинал (отметка на ЕПГУ)</th>\n')
                    file_html.write('                           <th rowspan="2">'
                                    'Договор на оказание платных образовательных услуг</th>\n')
                    file_html.write('                           <th rowspan="2">Приоритет</th>\n')
                    file_html.write('                           <th rowspan="2">Высший приоритет</th>\n')
                elif pk_name == 'spo' or pk_name == 'asp':
                    file_html.write('                           <th rowspan="2">Преимущественное право</th>\n')
                    if pk_name == 'spo':
                        colspan = 1
                    elif pk_name == 'asp':
                        colspan = 2
                    file_html.write(f'                           <th colspan="{colspan}">Результаты ВИ</th>\n')
                    file_html.write('                           <th rowspan="2">Сумма баллов за ИД</th>\n')
                    file_html.write('                           <th rowspan="2">Сдан оригинал</th>\n')
                    file_html.write('                           <th rowspan="2">Согласие на зачисление</th>\n')
                    file_html.write('                           <th rowspan="2">Статус</th>\n')
                    file_html.write('                           <th rowspan="2">Примечание</th>\n')
                    file_html.write('                           <th rowspan="2">Информация о зачислении</th>\n')

                file_html.write('                        </tr>\n')
                if len(l_short_title) > 0:
                    file_html.write('                        <tr>\n')
                # Названия вступительных испытаний
                    file_html.write('                           <th>' + str(l_short_title[0]) + '</th>\n')
                    if len(l_short_title) > 1:
                        file_html.write('                           <th>' + str(l_short_title[1]) + '</th>\n')
                        if len(l_short_title) > 2:
                            file_html.write('                           <th>' + str(l_short_title[2]) + '</th>\n')
                file_html.write('                        </tr>\n')
                file_html.write('                       </thead>\n')
                file_html.write('                       <tbody>\n')
                # Формируем строку по каждому студенту
                for a in range(len(l_number)):
                    file_html.write('                         <tr>\n')
                    file_html.write(f'                           <td>{l_number[a]}</td>\n')
                    """№"""
                    file_html.write(f'                           <td>{l_snils[a]}</td>\n')
                    """СНИЛС или Личный номер"""
                    file_html.write(f'                           <td>{l_total_points[a]}</td>\n')
                    """Сумма баллов"""
                    if pk_name == 'bak' or pk_name == 'mag':
                        # print(a, ' ', l_number[a])
                        vip_priority = ''
                        if l_req_comp_id_highest_priority[a] in row_priority:
                            vip_priority = 'Да'
                            # print(l_req_comp_id_highest_priority)
                        if pk_name == 'bak':
                            file_html.write(f'                           <td>{l_marks[a][0]}</td>\n')
                            """Результаты ВИ"""
                            file_html.write(f'                           <td>{l_marks[a][1]}</td>\n')
                            """Результаты ВИ"""
                            file_html.write(f'                           <td>{l_marks[a][2]}</td>\n')
                        elif pk_name == 'mag':
                            file_html.write(f'                           <td>{l_marks[a][0]}</td>\n')
                            """Результаты ВИ"""
                        """Результаты ВИ"""
                        file_html.write(f'                           <td>{l_total_points_id[a]}</td>\n')
                        """Сумма баллов за ИД"""
                        file_html.write(f'                           <td></td>\n')
                        """Основание приема без ВИ"""
                        file_html.write(f'                           <td>{l_preference_category_title[a]}</td>\n')
                        """Преимущественное право зачисления"""
                        file_html.write(f'                           <td>{l_original_passed[a]}</td>\n')
                        """Сдан оригинал (отметка на ЕПГУ)"""
                        file_html.write(f'                           <td></td>\n')
                        """Договор на оказание платных образовательных услуг"""
                        file_html.write(f'                           <td>{l_print_priority[a]}</td>\n')
                        """Приоритет"""
                        file_html.write(f'                           <td>{vip_priority}</td>\n')
                        """Высший приоритет (Да/'')"""
                    elif pk_name == 'spo' or pk_name == 'asp':
                        file_html.write(f'                           <td>{l_preference_category_title[a]}</td>\n')
                        """Преимущественное право"""
                        if pk_name == 'spo':
                            file_html.write(f'                           <td>{l_marks[a][0]}</td>\n')
                            """Результаты ВИ"""
                        elif pk_name == 'asp':
                            file_html.write(f'                           <td>{l_marks[a][0]}</td>\n')
                            """Результаты ВИ"""
                            file_html.write(f'                           <td>{l_marks[a][1]}</td>\n')
                            """Результаты ВИ"""
                        file_html.write(f'                           <td>{l_total_points_id[a]}</td>\n')
                        """Сумма баллов за ИД"""
                        file_html.write(f'                           <td>{l_original_passed[a]}</td>\n')
                        """Сдан оригинал"""
                        file_html.write(f'                           <td>{l_l_accepted[a]}</td>\n')
                        """Согласие на зачисление"""
                        file_html.write(f'                           <td>{l_status[a]}</td>\n')
                        """Статус"""
                        file_html.write(f'                           <td></td>\n')
                        """Примечание"""
                        file_html.write(f'                           <td></td>\n')
                        """Информация о зачислении"""

                # Закрываем таблицу для конкурса
                file_html.write('                       </tbody>\n')
                file_html.write('                     </table>\n')
                file_html.write('                  </div>\n')
            # Заканчиваем формирования блока по каждому направлению
            if (edu_program_form is not None) and (plan_recruitment is not None):
                file_html.write(f'                  <p> Заявлений — {statement}, '
                                f'число мест — {s_plan_recruitment}</p>\n')
            if faculty is not None:
                file_html.write('                  <hr>\n')
    # Завершаем формирования html страница
    file_html.write('            </div>\n')
    file_html.write('         </div>\n')
    file_html.write('      </div>\n')
    file_html.write('   </body>\n')
    file_html.write('</html>')
    # Закрываем работу с файлом
    file_html.close()
