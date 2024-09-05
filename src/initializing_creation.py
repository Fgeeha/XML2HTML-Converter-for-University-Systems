import gzip
import os
import shutil
from datetime import datetime
from zipfile import ZipFile

from src.core.config import settings
from src.template.crete_html import create_html


def check_dir(dir_name: str) -> None:
    if not os.path.exists(f"{dir_name}"):
        os.makedirs(f"{dir_name}")


def main():
    debug_mode = settings.app.debug
    # Настройки Даты и Время
    data_time_now = datetime.now()
    data_time_now = data_time_now.strftime("%d%m%Y %H-%M-%S")
    dt_now = str(data_time_now)

    file_name_enr_recommended_bak = (
        settings.app.file_name_enr_recommended_bak
    )  # Название файлов для высшего приоритета
    file_name_enr_recommended_mag = (
        settings.app.file_name_enr_recommended_mag
    )  # Название файлов для высшего приоритета

    dir_name_file_priority = (
        "file_priority"  # Название директории где будет высший приоритет
    )

    name_pk = (
        settings.app.name_pk
    )  # словарь ( краткое название ПК : названия файла до расширения)

    if not debug_mode:
        check_dir("dump")
        os.mkdir(f"dump/{dt_now}")

    for pk_title in name_pk:
        if pk_title in ("bak", "mag"):
            file_name_enr_recommended = ""

            if os.path.exists(dir_name_file_priority):
                shutil.rmtree(dir_name_file_priority)
            os.mkdir(dir_name_file_priority)

            if pk_title == "mag":
                file_name_enr_recommended = file_name_enr_recommended_mag
            elif pk_title == "bak":
                file_name_enr_recommended = file_name_enr_recommended_bak

            if os.path.exists(file_name_enr_recommended):
                with ZipFile(file_name_enr_recommended, "r") as my_zip:
                    my_zip.extractall(path=dir_name_file_priority)
                    my_zip.close()
                if not debug_mode:
                    shutil.move(
                        file_name_enr_recommended,
                        f"dump/{dt_now}/{file_name_enr_recommended}",
                    )

        if os.path.exists(f"{name_pk[pk_title]}.xml.zip"):
            if os.path.exists(f"{name_pk[pk_title]}.xml"):
                try:
                    os.remove(f"{name_pk[pk_title]}.xml")
                except OSError as e:
                    print(f"Error: {e.filename} - {e.strerror}.")

            with gzip.open(f"{name_pk[pk_title]}.xml.zip", "rb") as f_in:
                with open(f"{name_pk[pk_title]}.xml", "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            create_html(
                pk_name=pk_title,
                file_xml_name=f"{name_pk[pk_title]}",
                dir_name_for_priority=dir_name_file_priority,
            )

            if not debug_mode:
                if os.path.exists(dir_name_file_priority):
                    shutil.move(
                        dir_name_file_priority,
                        f"dump/{dt_now}/dir_name_file_priority",
                    )
                shutil.move(
                    f"{name_pk[pk_title]}.xml.zip",
                    f"dump/{dt_now}/{name_pk[pk_title]}.xml.zip",
                )

    if not debug_mode:
        if os.path.exists(dir_name_file_priority):
            shutil.rmtree(dir_name_file_priority)


if __name__ == "__main__":
    main()
