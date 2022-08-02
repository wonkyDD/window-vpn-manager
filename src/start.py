# TODO :
# 패키지파일이 아닌 script 파일.
#
# script/ 로 옮길 수 없는 이유는
# from src.database import backup_database로 수정해야 하는데
# 이런 식의 import는 최상단 루트에서만 할 수 있는 것.
#
# src라는 모듈을 찾을 수 없다고 에러가 뜬다
# 물론 from ..src.database 로 고치면 no parent package에러가 뜬다
#
# 위와 같은 이유가 있으므로
# 타입 ignore를 통해 mypy에서 제외시킨다.
#
# TODO : mypy.ini에서 특정파일에 대한 exclude 지원이 안되는 건가?

import os
import sqlite3
from datetime import datetime

from database import backup_database, get_database  # type: ignore # pylint: disable=E0401

# TODO :
# 타입 ignore를 block으로 설정하는 방법은 없나?
from settings import DRIVER_TYPES, KOR_DEST, WEEKDAYS  # type: ignore # pylint: disable=E0401
from YdManager import YdManager  # type: ignore # pylint: disable=E0401


def make_directory():
    date = datetime.now()
    pref = "."
    sep = "_"
    y = str(date.year)
    m = "0" + str(date.month) if date.month < 10 else str(date.month)
    d = str(date.day)
    wd = WEEKDAYS[datetime.today().weekday()]

    DIRNAME = pref + y + sep + m + sep + d + sep + wd
    if not os.path.exists(KOR_DEST + DIRNAME):
        try:
            os.mkdir(KOR_DEST + DIRNAME)
        except FileNotFoundError as exc:
            # TODO : Logger로 교체
            print("\n\nWRONG PATH >> " + exc.filename)
            print(exc.args[1] + "\n\n")


def insert():
    backup_database()
    yd_manager.renew_videoid_table()


def fetch():
    db_address = get_database()

    try:
        db = sqlite3.connect(db_address)

        with db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()

            cur.execute(
                """
                        SELECT korean_porn, korean_bj, asian_porn_movies, china_porn FROM videoId 
                        ORDER BY id DESC 
                        LIMIT 1 OFFSET 1
                        """
            )
            row = cur.fetchone()
            print_datas = {}
            for key in row.keys():
                print_datas.update({key: row[key]})

            print(print_datas)

    except Exception as exc:
        # TODO : logger로 교체
        print(str(exc).encode("utf-8"))

    finally:
        if db:
            db.close()


if __name__ == "__main__":
    make_directory()
    backup_database()

    yd_manager = YdManager(DRIVER_TYPES.get("firefox"))
    insert()
    fetch()
    yd_manager.exit_driver()
