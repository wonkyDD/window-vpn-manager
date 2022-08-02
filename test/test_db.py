import sqlite3
from typing import Dict, List

from src.database import get_database


def fetch(error: bool = False) -> List[Dict]:
    db_address = get_database()

    try:
        db = sqlite3.connect(db_address)
        with db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()

            if error:
                raise Exception
            else:
                cur.execute(
                    """
                            SELECT * FROM videoId 
                            ORDER BY id DESC 
                            """
                )
            rows = cur.fetchall()
        return rows

    except Exception as exc:
        # TODO : logger로 교체
        print(str(exc).encode("utf-8"))
        return []
    finally:
        if db:
            db.close()


def test_fetch():
    rows = fetch()
    assert rows, "해당 db테이블에 insert된 데이터가 없습니다"
    assert len(rows) == rows[0]["id"], "해당 db테이블에 예기치않은 데이터 삭제가 발생"

    assert not fetch(True)
