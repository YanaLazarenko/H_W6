import sys
from pathlib import Path
from normalize import normalize
import shutil
import uuid


CATEGORIES = {'Audio': ['.mp3'],
              'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt'],
              'Images': ['.png', '.jpeg'],
              'Other': [],
              'Video': ['.avi', '.mkv'],
              'Archives': ['.zip', '.rar']}


def unpack_archive(path: Path) -> None:
    archive_folder = "Archives"
    try:
        for item in path.glob(f"{archive_folder}/*"):
            filename = item.stem
            arh_dir = path.joinpath(path / archive_folder / filename)
            arh_dir.mkdir()
            shutil.unpack_archive(item, arh_dir)
    except:
        FileExistsError


def delete_empty_folder(path: Path) -> None:
    folders_to_delete = [f for f in path.glob('**')]
    try:
        for folder in folders_to_delete[::-1]:
            folder.rmdir()
    except:
        OSError


def move_file(path: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f'{normalize(path.stem)}{path.suffix}')
    if new_name.exists():
        print(new_name)
        new_name = new_name.with_name(
            f'{new_name.stem}-{uuid.uuid4()}{path.suffix}')
    path.rename(new_name)


def get_categories(path: Path) -> str:
    ext = path.suffix.lower()
    for categorie, extantion in CATEGORIES.items():
        if ext in extantion:
            return categorie
    return 'Other'


def sort_folder(path: Path) -> None:
    for item in path.glob('**/*'):
        # print(item)
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError as e:
        return 'No path to folder'

    if not path.exists():
        return f'Folder path {path} doesn"t exists'

    sort_folder(path)
    unpack_archive(path)
    sort_folder(path)
    delete_empty_folder(path)

    return 'All ok'


if __name__ == '__main__':
    main()
