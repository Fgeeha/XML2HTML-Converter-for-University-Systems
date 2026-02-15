import gzip
import logging
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

from src.core.config import settings
from src.template.create_html import create_html


logger = logging.getLogger(__name__)


def ensure_directory(path: Path) -> None:
    """Создает директорию, если она не существует."""
    path.mkdir(parents=True, exist_ok=True)


def timestamped_dump_dir(base_dir: Path, debug: bool) -> Path:
    """Подготавливает директорию dump с временной меткой (если не debug)."""
    if debug:
        return base_dir

    now = datetime.now().strftime(settings.app.date_time_format)
    dump_dir = base_dir / now
    ensure_directory(base_dir)
    ensure_directory(dump_dir)
    return dump_dir


def extract_priority_zip(
    zip_path: Path,
    dest_dir: Path,
    dump_dir: Path,
    debug: bool,
) -> None:
    """Извлекает zip-архив приоритетов и опционально перемещает его в dump."""
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    ensure_directory(dest_dir)

    with ZipFile(zip_path, "r") as archive:
        archive.extractall(dest_dir)

    logger.info("Извлечен архив приоритетов: %s", zip_path.name)

    if not debug:
        shutil.move(str(zip_path), str(dump_dir / zip_path.name))


def decompress_xml(zip_path: Path, xml_path: Path) -> None:
    """Распаковывает .xml.zip в .xml, удаляя существующий xml при наличии."""
    if xml_path.exists():
        xml_path.unlink()

    with gzip.open(zip_path, "rb") as f_in, xml_path.open("wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    logger.info("Распакован XML: %s -> %s", zip_path.name, xml_path.name)


def process_pk(
    pk_key: str,
    names: dict[str, str],
    priority_dir: Path,
    dump_dir: Path,
    debug: bool,
) -> None:
    """Обрабатывает извлечение, декомпрессию, генерацию HTML и перемещение файлов для ПК."""
    logger.info("Обработка ПК: %s", pk_key)

    if pk_key in ("bak", "mag"):
        zip_name = settings.app.file_name_enr_recommended.get(pk_key, "")
        zip_path = Path(zip_name)
        if zip_path.exists():
            extract_priority_zip(zip_path, priority_dir, dump_dir, debug)

    base_name = names[pk_key]
    xml_zip = Path(f"{base_name}.xml.zip")
    xml_file = Path(f"{base_name}.xml")

    if not xml_zip.exists():
        logger.warning("Файл не найден: %s", xml_zip)
        return

    decompress_xml(xml_zip, xml_file)
    create_html(
        pk_name=pk_key,
        file_xml_name=base_name,
        dir_name_for_priority=str(priority_dir),
    )

    if not debug:
        if priority_dir.exists():
            shutil.move(str(priority_dir), str(dump_dir / priority_dir.name))
        shutil.move(str(xml_zip), str(dump_dir / xml_zip.name))


def main() -> None:
    """Главная функция приложения."""
    debug = settings.app.debug
    dump_base = Path("dump")
    priority_dir = Path(settings.app.dir_name_file_priority)
    pk_map = settings.app.name_pk

    logger.info("Запуск обработки (debug=%s)", debug)

    dump_dir = timestamped_dump_dir(dump_base, debug)

    for pk in pk_map:
        process_pk(pk, pk_map, priority_dir, dump_dir, debug)

    if not debug and priority_dir.exists():
        shutil.rmtree(priority_dir)

    logger.info("Обработка завершена")


if __name__ == "__main__":
    main()
