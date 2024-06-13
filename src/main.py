# src/main.py
from templates.createhtml import create_html
from utils import check_dir
import os
import logging
from zipfile import ZipFile
import gzip
import shutil
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    debug_mode = True
    """
    False - transferring files to a folder dump
    True - zip archives remain in the root folder
    """

    if not debug_mode:
        data_time_now = datetime.now()
        data_time_format = "%d%m%Y %H-%M-%S"
        dt_now = data_time_now.strftime(data_time_format)

    file_name_enr_recommended_bak = 'enr_recommended_enrollment_list_1747824879895441661.zip'
    file_name_enr_recommended_mag = 'enr_recommended_enrollment_list_1747848868372017405.zip'
    dir_name_file_priority = 'file_priority'
    name_pk = {
        'bak': 'enr_rating_1780165749254516989',
        'mag': 'enr_rating_1747848868372017405',
        'spo': 'enr_rating_1756521485483241725',
        'asp': 'enr_rating_1780891192879345917'
    }

    if not debug_mode:
        check_dir('dump')
        os.mkdir(f'dump/{dt_now}')

    for pk in name_pk:
        if pk in ['mag', 'bak']:
            file_name_enr_recommended = ''
            if os.path.exists(dir_name_file_priority):
                shutil.rmtree(dir_name_file_priority)
            os.mkdir(dir_name_file_priority)
            file_name_enr_recommended = file_name_enr_recommended_mag if pk == 'mag' else file_name_enr_recommended_bak
            if os.path.exists(file_name_enr_recommended):
                with ZipFile(file_name_enr_recommended, "r") as myzip:
                    myzip.extractall(path=dir_name_file_priority)
                if not debug_mode:
                    shutil.move(file_name_enr_recommended, f'dump/{dt_now}/{file_name_enr_recommended}')

        if os.path.exists(f'{name_pk[pk]}.xml.zip'):
            if os.path.exists(f'{name_pk[pk]}.xml'):
                try:
                    os.remove(f'{name_pk[pk]}.xml')
                except OSError as e:
                    logging.error(f"Error: {e.filename} - {e.strerror}.")

            with gzip.open(f"{name_pk[pk]}.xml.zip", 'rb') as f_in:
                with open(f"{name_pk[pk]}.xml", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            create_html(pk_name=pk, file_xml_name=f'{name_pk[pk]}', dir_name_for_priority=dir_name_file_priority)
            os.remove(f'{name_pk[pk]}.xml')

            if os.path.exists(dir_name_file_priority):
                shutil.rmtree(dir_name_file_priority)

            if not debug_mode:
                shutil.move(f'{name_pk[pk]}.xml.zip', f'dump/{dt_now}/{name_pk[pk]}.xml.zip')

    if not debug_mode and os.path.exists(dir_name_file_priority):
        shutil.rmtree(dir_name_file_priority)

if __name__ == '__main__':
    main()
