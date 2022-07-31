from pathlib import Path

WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

DRIVER_TYPES = {
    'firefox'   : 'Firefox',
    'chrome'    : 'Chrome',
}

TARGET_LINKS = {
    'korean-porn'           : 'https://kissjav.li/videos/korean-porn/',
    'korean-bj'             : 'https://kissjav.li/videos/korean-bj/',
    'asian-porn-movies'     : 'https://kissjav.li/videos/asian-porn-movies/',
    'china-porn'            : 'https://kissjav.li/videos/china-porn/',
}

SCREENSHOT_NAMES = {
    'korean-porn' : 'korean-porn.png',
    'korean-bj' : 'korean-bj.png',
    'asian-porn-movies' : 'asian-porn-movies.png',
    'china-porn' : 'china-porn.png'
}
SCREENSHOT_PATH = str(Path(__file__).parent.parent) + '\\materials\\screenshots\\'


SRC         = 'C:\\Users\\USER\\Downloads\\'
KOR_DEST    = 'Z:\\Korea\\kissjav\\'
CHN_DEST    = 'Z:\\.CHINA\\'
MOV_DEST    = 'Z:\\.MOVIE\\'

DB_NAME     = 'test.db'
# DB_NAME     = 'ydmanager.db'
DB_PATH = str(Path(__file__).parent.parent) + '\\db\\'
BACKUP_SQL_NAME = 'ydmanager.sql'
BACKUP_SQL_PATH = str(Path(__file__).parent.parent.parent.parent) + '\\__BACKUP__\\'

DB_TABLE_NAMES = [
    'videoId',
]

TXT_NAME    = 'ydmanager.txt'
TXT_PATH    = str(Path(__file__).parent.parent) + '\\'

LOG_NAME = 'ydmanager.log'
LOG_PATH = str(Path(__file__).parent.parent) + '\\log\\'


# ACTIONS = []
# ACTIONS_DELAY = {}
