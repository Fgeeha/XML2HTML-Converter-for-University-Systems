import shutil
import gzip
from zipfile import ZipFile
from datetime import datetime
from pathlib import Path

from src.core.config import settings
from src.template.crete_html import create_html


def ensure_directory(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def timestamped_dump_dir(base_dir: Path, debug: bool) -> Path:
    """Prepare a dump directory with a timestamp if not in debug mode."""
    if debug:
        return base_dir  # no dumping in debug mode

    now = datetime.now().strftime("%d%m%Y %H-%M-%S")
    dump_dir = base_dir / now
    ensure_directory(base_dir)
    ensure_directory(dump_dir)
    return dump_dir


def extract_priority_zip(
    zip_path: Path, dest_dir: Path, dump_dir: Path, debug: bool
) -> None:
    """Extract a priority zip file and optionally move it to dump."""
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    ensure_directory(dest_dir)

    with ZipFile(zip_path, "r") as archive:
        archive.extractall(dest_dir)

    if not debug:
        shutil.move(str(zip_path), str(dump_dir / zip_path.name))


def decompress_xml(zip_path: Path, xml_path: Path) -> None:
    """Decompress a .xml.zip into .xml, removing existing xml if present."""
    if xml_path.exists():
        xml_path.unlink()

    with gzip.open(zip_path, "rb") as f_in, xml_path.open("wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def process_pk(
    pk_key: str, names: dict, priority_dir: Path, dump_dir: Path, debug: bool
) -> None:
    """Handle extraction, decompression, HTML creation, and dumping for a given pk."""
    # Priority extraction for 'bak' or 'mag'
    if pk_key in ("bak", "mag"):
        zip_name = (
            settings.app.file_name_enr_recommended_bak
            if pk_key == "bak"
            else settings.app.file_name_enr_recommended_mag
        )
        zip_path = Path(zip_name)
        if zip_path.exists():
            extract_priority_zip(zip_path, priority_dir, dump_dir, debug)

    # Decompress XML
    base_name = names[pk_key]
    xml_zip = Path(f"{base_name}.xml.zip")
    xml_file = Path(f"{base_name}.xml")

    if xml_zip.exists():
        decompress_xml(xml_zip, xml_file)
        create_html(
            pk_name=pk_key,
            file_xml_name=base_name,
            dir_name_for_priority=str(priority_dir),
        )

        if not debug:
            # Move priority directory
            if priority_dir.exists():
                shutil.move(str(priority_dir), str(dump_dir / priority_dir.name))
            # Move the source zip
            shutil.move(str(xml_zip), str(dump_dir / xml_zip.name))


def main() -> None:
    debug = settings.app.debug
    dump_base = Path("dump")
    priority_dir = Path("file_priority")
    pk_map = settings.app.name_pk

    dump_dir = timestamped_dump_dir(dump_base, debug)

    for pk in pk_map:
        process_pk(pk, pk_map, priority_dir, dump_dir, debug)

    # Clean up priority directory
    if not debug and priority_dir.exists():
        shutil.rmtree(priority_dir)


if __name__ == "__main__":
    main()
