"""
총 개수 테이블:
row 한도는 정해져있지않고, column은 id, day, total 7개로 끝난다

각 개수 테이블
총개수테이블의 row id를 공유해서, 장르별로 개수를 추가로 정리
row 한도는 정해져있지않고, column은 id(primary), id(공유), genre, num 4개로 끝난다

"""


# TODO : FILE 이동
#
# 0. shutil은 다음과 같은 이슈에 대해 어떻게 처리하는지 소스코드보고 분석
# - 파일 중복
# - 파일 대용량 이동
# - 파일 이동완료 / 미완료 이벤트는 어떻게 다루는지?
#
# 
# 1. 0번 분석 기반으로, locate.py 수정 
# 2. 0번을 기반으로 확신이 든다면, #life.ps1을 알맞게 수정


# TODO : 
# 2. 파일이동전에는 용량을 읽어온다
# 3. sqlite로 용량은 따로 로컬db에 저장


from datetime import datetime
import os
import shutil

WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'] 
SRC = 'C:\\Users\\USER\\Downloads\\'
KOR_DEST = 'Z:\\Korea\\kissjav\\'
CHN_DEST = 'Z:\\.CHINA\\'
MOV_DEST = 'Z:\\.MOVIE\\'


def locate(genre: str):
    get_files = os.listdir(SRC)
    
    if(genre == 'kor'):
        date = datetime.now()
        pref = '.'
        sep = '_'
        y = str(date.year)
        m = '0' + str(date.month) if date.month < 10 else str(date.month)
        d = str(date.day)
        wd = WEEKDAYS[datetime.today().weekday()]

        DIRNAME = pref + y + sep + m + sep + d + sep + wd

        if(not os.path.exists(KOR_DEST + DIRNAME)):
            os.mkdir(KOR_DEST + DIRNAME)
        
        # TODO : 중복이름에 대해 어떻게 처리하는지?
        for f in get_files:
            shutil.move(SRC + f, KOR_DEST)        
        
    if(genre == 'chn'):
        # TODO : 중복이름에 대해 어떻게 처리하는지?
        for f in get_files:
            shutil.move(SRC + f, CHN_DEST)
        
    if(genre == 'mov'):
        # TODO : 중복이름에 대해 어떻게 처리하는지?
        for f in get_files:
            shutil.move(SRC + f, MOV_DEST)
