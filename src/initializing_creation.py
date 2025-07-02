import gzip
import os
import shutil
from datetime import datetime
from zipfile import ZipFile

from src.core.config import settings
from src.template.crete_html import create_html


def check_and_create_dir(dir_name: str) -> None:
    """Создаёт директорию, если её нет."""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def extract_zip(file_name: str, extract_to: str) -> None:
    """Распаковывает zip-архив в указанную папку."""
    with ZipFile(file_name, "r") as my_zip:
        my_zip.extractall(path=extract_to)


def move_file(src: str, dst: str) -> None:
    """Перемещает файл или папку."""
    if os.path.exists(src):
        shutil.move(src, dst)


def decompress_gzip(input_file: str, output_file: str) -> None:
    """Распаковывает gzip-файл в обычный файл."""
    with gzip.open(input_file, "rb") as f_in, open(output_file, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def prepare_dump_dir(debug_mode: bool, dt_now: str) -> None:
    """Создаёт папку dump и поддиректорию с датой, если не debug."""
    if not debug_mode:
        check_and_create_dir("dump")
        os.mkdir(f"dump/{dt_now}")


def process_priority_zip(pk_title: str, file_name: str, dir_priority: str, dt_now: str, debug_mode: bool) -> None:
    """Обрабатывает zip-файл с приоритетами для бакалавриата и магистратуры."""
    if os.path.exists(dir_priority):
        shutil.rmtree(dir_priority)
    os.mkdir(dir_priority)
    extract_zip(file_name, dir_priority)
    if not debug_mode:
        move_file(file_name, f"dump/{dt_now}/{file_name}")


def process_xml_gzip(pk_title: str, name_pk: dict, dir_priority: str, dt_now: str, debug_mode: bool) -> None:
    """Обрабатывает основной xml.gz файл: распаковка, генерация html, перемещение файлов."""
    xml_gz = f"{name_pk[pk_title]}.xml.zip"
    xml_file = f"{name_pk[pk_title]}.xml"
    if os.path.exists(xml_gz):
        if os.path.exists(xml_file):
            try:
                os.remove(xml_file)
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}.")
        decompress_gzip(xml_gz, xml_file)
        create_html(
            pk_name=pk_title,
            file_xml_name=name_pk[pk_title],
            dir_name_for_priority=dir_priority,
        )
        if not debug_mode:
            if os.path.exists(dir_priority):
                move_file(dir_priority, f"dump/{dt_now}/dir_name_file_priority")
            move_file(xml_gz, f"dump/{dt_now}/{xml_gz}")


def main():
    """Главная функция: обработка всех этапов создания html-отчётов по приёмной кампании."""
    debug_mode = settings.app.debug
    data_time_now = datetime.now().strftime("%d%m%Y %H-%M-%S")
    dt_now = str(data_time_now)
    file_name_enr_recommended_bak = settings.app.file_name_enr_recommended_bak
    file_name_enr_recommended_mag = settings.app.file_name_enr_recommended_mag
    name_pk = settings.app.name_pk
    dir_name_file_priority = settings.app.dir_name_file_priority
    prepare_dump_dir(debug_mode, dt_now)
    for pk_title in name_pk:
        if pk_title in ("bak", "mag"):
            file_name_enr_recommended = file_name_enr_recommended_mag if pk_title == "mag" else file_name_enr_recommended_bak
            process_priority_zip(pk_title, file_name_enr_recommended, dir_name_file_priority, dt_now, debug_mode)
        process_xml_gzip(pk_title, name_pk, dir_name_file_priority, dt_now, debug_mode)
    if not debug_mode and os.path.exists(dir_name_file_priority):
        shutil.rmtree(dir_name_file_priority)


if __name__ == "__main__":
    main()
