"""
TODO :
ImportError: cannot import name 'YdManager' 
from partially initialized module 'YdManager' 
(most likely due to a circular import)

from YdManager import YdManager
"""

import re
import sqlite3
from typing import Dict, List, Tuple

from multipledispatch import dispatch

from .database import get_database
from .settings import DB_TABLE_NAMES, TARGET_LINKS


def timer(elapsed_time: float) -> float:
    # min, sec로 변환
    if elapsed_time >= 60.0:
        minute = int(elapsed_time // 60)
        sec = elapsed_time - (minute * 60.0)
        print(f"Taken time : {minute}min {round(sec, 1)}sec")

    else:
        print(f"Taken time : {round(elapsed_time, 1)}sec")

    return elapsed_time


@dispatch(dict)  # type: ignore
def dash_to_underscore(old_datas: Dict[str, str]) -> Dict[str, str]:
    changed_datas = {}
    for genre, target in old_datas.items():

        # TODO : split delmiter not keep
        pattern = "(-)"
        s = re.split(pattern, genre)

        new_key = ""
        for i in range(len(s)):
            if s[i] == "-":
                s[i] = "_"
            new_key += s[i]

        changed_datas.update({new_key: target})

    return changed_datas


@dispatch(str)  # type: ignore
def dash_to_underscore(data: str) -> str:
    pattern = "(-)"
    s = re.split(pattern, data)

    new_data = ""
    for i in range(len(s)):
        if s[i] == "-":
            s[i] = "_"
        new_data += s[i]

    return new_data


# TODO :
# start.py에서 반드시 insert전에 호출
def count_uploaded_videos(yd_manager) -> Dict[str, int]:
    db_address = get_database()

    try:
        db = sqlite3.connect(db_address)
        with db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            videoid_table_name = [name for name in DB_TABLE_NAMES if name == "videoId"][
                0
            ]

            cur.execute(
                f"""
                        SELECT korean_porn, korean_bj, asian_porn_movies, china_porn FROM {videoid_table_name} 
                        ORDER BY id DESC 
                        LIMIT 1 
                        """
            )
            row = cur.fetchone()

        for key in row.keys():
            print(key, row[key])

        # TODO : db 접근이 끝났으니까 with밖에서 하는게 맞는가?
        uploaded_counts = {}
        for genre, target_link in TARGET_LINKS.items():

            target_video_id = int(row[dash_to_underscore(genre)])
            count = 0
            page_num = 1

            while True:
                if page_num == 1:
                    yd_manager.get(target_link)
                else:
                    yd_manager.get(target_link + str(page_num))

                titles_and_links: List[
                    Tuple[str, str]
                ] = yd_manager.get_all_videolinks()

                videoids = []
                for title_and_link in titles_and_links:
                    link = title_and_link[1]

                    videoid: int = int(yd_manager.parse_videoid(link))
                    videoids.append(videoid)

                # TODO : 게시물이 삭제되서 남아있지 않은 경우가 있어서..
                # 빠짐없이 내림차순이 된다고 억지 가정을 해버렸다.
                is_found = False
                for i in range(len(videoids)):
                    if target_video_id >= videoids[i]:
                        is_found = True
                        count += i
                        break

                if not is_found:
                    count += len(videoids)
                    page_num += 1

                else:
                    uploaded_counts.update({genre: count})
                    break

        return uploaded_counts

    except Exception as exc:
        # TODO : logger로 교체
        print(str(exc).encode("utf-8"))
        return {}
    finally:
        if db:
            db.close()
