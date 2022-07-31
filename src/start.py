import os
import sqlite3

from settings import WEEKDAYS, KOR_DEST
from datetime import datetime

from settings import (
    DRIVER_TYPES,
)
from YdManager import YdManager
from database import get_database, backup_database
from src.util import count_uploaded_videos


def make_directory():
    date = datetime.now()
    pref = '.'
    sep = '_'
    y = str(date.year)
    m = '0' + str(date.month) if date.month < 10 else str(date.month)
    d = str(date.day)
    wd = WEEKDAYS[datetime.today().weekday()]

    DIRNAME = pref + y + sep + m + sep + d + sep + wd

    if(not os.path.exists(KOR_DEST + DIRNAME)):
        try:
            os.mkdir(KOR_DEST + DIRNAME)
        except FileNotFoundError as exc:
            # TODO : Logger로 교체
            print('\n\nWRONG PATH >> ' + exc.filename)
            print(exc.args[1] + '\n\n')


def insert():
    yd_manager = YdManager(DRIVER_TYPES.get('firefox'))
    backup_database()
    yd_manager.renew_videoid_table()


def fetch():
    db_address = get_database()
    
    try:
        db = sqlite3.connect(db_address)
        
        with db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            
            cur.execute("""
                        SELECT korean_porn, korean_bj, asian_porn_movies, china_porn FROM videoId 
                        ORDER BY id DESC 
                        LIMIT 1 OFFSET 1
                        """)
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
    

if __name__ == '__main__':
    make_directory()
    backup_database()
    
    yd_manager = YdManager(DRIVER_TYPES.get('firefox'))
    
    # 반드시 insert전에 호출
    count_uploaded_videos(yd_manager)
    
    insert()
    fetch()
    
    yd_manager.exit_driver()