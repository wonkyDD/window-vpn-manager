import os
from typing import List

SRC = os.path.dirname(__file__) + "\\ps1\\"
DEST = "D:\\dev\\"
BACKUP_DEST = "D:\\dev\\__BACKUP__\\"

dest_files = os.listdir(DEST)
dest_files = list(filter(lambda dest_file: dest_file.endswith(".ps1"), dest_files))

src_files = os.listdir(SRC)
src_files = list(filter(lambda src_file: src_file.endswith(".ps1"), src_files))


def sync_file_num(src_files: List[str], dest_files: List[str]):  # pylint: disable=W0621
    # DELETE : src에 없는데 dev에는 남아있는 경우, dev에서 삭제
    for dest_file in dest_files:
        dest_file_path = DEST + dest_file
        if not os.path.isfile(SRC + dest_file):
            print("yes")
            os.remove(dest_file_path)

    # ADD : scr에 있는데 dev에는 없는 경우, dev에 추가
    for src_file in src_files:
        dest_file_path = DEST + src_file
        if not os.path.isfile(dest_file_path):
            with open(dest_file_path, "w", encoding="UTF-8"):
                pass


def sync_file_context(
    src_files: List[str], dest_files: List[str]
):  # pylint: disable=W0621
    dest_files = os.listdir(DEST)
    dest_files = list(filter(lambda dest_file: dest_file.endswith(".ps1"), dest_files))

    for src_file in src_files:
        src_file_path = SRC + src_file
        dest_file_path = DEST + src_file

        for dest_file in dest_files:
            if dest_file == src_file:
                with open(src_file_path, "r", encoding="UTF-8") as f:
                    src_datas = f.readlines()

                with open(dest_file_path, "w", encoding="UTF-8") as f:
                    f.writelines(src_datas)

                break


def backup(src_files: List[str], backup_path: str):  # pylint: disable=W0621
    if not os.path.exists(backup_path):
        os.mkdir(backup_path)

    for src_file in src_files:
        src_file_path = SRC + src_file

        with open(src_file_path, "r", encoding="UTF-8") as f:
            src_datas = f.readlines()

        with open(backup_path + src_file, "w", encoding="UTF-8") as f:
            f.writelines(src_datas)


backup(src_files, BACKUP_DEST)
sync_file_num(src_files, dest_files)
sync_file_context(src_files, dest_files)
