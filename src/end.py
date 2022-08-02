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
# 타입 ignorer를 통해 mypy에서 제외시킨다.
#
# TODO : mypy.ini에서 특정파일에 대한 exclude 지원이 안되는 건가?


from database import backup_database  # type: ignore # pylint: disable=E0401

if __name__ == "__main__":
    backup_database()
