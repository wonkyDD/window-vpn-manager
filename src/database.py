"""
TODO :
https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta

TODO : 
comma를 뒤에 안붙여주면 에러가 난다
cur.execute('INSERT INTO test (name) VALUES(?)', ('chally',))

TODO : executemany를 할때는 ...
1. column을 명시하고, 
2. values안에도 :컬럼이름 으로 명시를 해주고
3. [] 안에는 dict로 넣어줘야만 제대로 실행이 된다
cur.executemany('INSERT INTO test (name) VALUES(?)', [('a'),('b'),('v'),('ax'),]) << 에러!
cur.executemany('INSERT INTO test (name) VALUES(:name)', [{'name': 'james'}, {'name': 'amy'}]) << 통과!

"""


"""
TODO : 다운로더, shutil 관련 숙지가 끝나야 고려가능하다

용량 테이블:
row 한도는 정해져있지않고, column은 id, day, volume 3개로 끝난다

장르별 용량테이블:
용량테이블의 row id를 공유해서, 장르별로 용량을 추가로 정리
row 한도는 정해져있지않고, column은 id(primary), id(공유), genre, volume 4개로 끝난다
(앞으로 장르 4개에 맞춰서 다운로드할때도 지키면서하자)

다운로드에 걸린시간 테이블:
row 한도는 정해져있지않고, column은 id, day, elapsedtime 3개로 끝난다
"""

import sqlite3
import os
from typing import List
from settings import (
    DB_NAME, 
    DB_PATH, 
    DB_TABLE_NAMES,
    BACKUP_SQL_NAME,
    BACKUP_SQL_PATH,
)


# TODO : TEXT로 들고있다가 나중에 쓸때 int로 변환해서 쓰는 게 맞는건가?
SQL_CREATE_VIDEOID_TABLE = """
    CREATE TABLE IF NOT EXISTS `videoId`(
        `id`                    INTEGER PRIMARY KEY AUTOINCREMENT,
        `created`               DATETIME DEFAULT (datetime('now','localtime')) NOT NULL,
        `korean_porn`           TEXT NOT NULL,
        `korean_bj`             TEXT NOT NULL,
        `asian_porn_movies`     TEXT NOT NULL,
        `china_porn`            TEXT NOT NULL);"""


def create_database(db_address: str):
    try:
        db = sqlite3.connect(db_address)
        with db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            create_tables(cur, DB_TABLE_NAMES)
            db.commit()

    except Exception as exc:
        print(str(exc).encode("utf-8"))

    finally:
        if db:
            db.close()


def get_database(make: bool = False) -> str:
    if not os.path.isfile(DB_PATH + DB_NAME) or make:
        create_database(DB_PATH + DB_NAME)
    
    return DB_PATH + DB_NAME


def create_tables(cur: sqlite3.Cursor, tables: List[str]):
    if 'videoId' in tables:
        cur.execute(SQL_CREATE_VIDEOID_TABLE)
    
    if 'volume' in tables:
        pass


# TODO : https://www.geeksforgeeks.org/how-to-create-a-backup-of-a-sqlite-database-using-python/
# SQL문으로 백업해놓는게 옳을까?
def backup_database():
    db_address = get_database()
    try:
        db = sqlite3.connect(db_address)
        with db:
            with open(f"{BACKUP_SQL_PATH}{BACKUP_SQL_NAME}", 'w') as p: 
                for line in db.iterdump(): 
                    p.write('%s\n' % line)
            
    except Exception as exc:
        print(str(exc).encode("utf-8"))
    
    finally:
        if db:
            db.close()
