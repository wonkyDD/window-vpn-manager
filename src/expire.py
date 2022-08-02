import os
import subprocess
from datetime import datetime

SRC = "./temp.txt"
EXPIRE_INDEX = 2

with open(SRC, "r", encoding="utf-8") as f:
    data = f.readlines()

d = data[EXPIRE_INDEX]
s = d.split(" ")

# TODO : 만약 cli api 출력 형식이 바뀌게 된다면?
assert s[0] == "Expires" and s[1] == "at"

# TODO : 추후에 자동갱신 혹은 gui 알리미 같은게 있으면 좋겠다
time_info = s[-3:]
expire_date = datetime.strptime(time_info[0], "%Y-%m-%d")
now = datetime.now()
diff = expire_date - now


# TODO :
# diff.days 와 hour 를 읽어서 몇일 몇시간남았다고 image generate하는게 있었으면 좋겠다


if diff.days > 7:
    # subprocess.call('ascii-image-converter ..\materials\warning1.jfif')
    print("expire까지 남은 시간")
    print("///////////////")
    print("")
    print(str(diff.days) + "days" + "   " + str(round(diff.seconds / 3600)) + "hours")
    print("")
    print("///////////////")

else:
    subprocess.call("ascii-image-converter ..\materials\warning1.jfif")
    print("expire까지 남은 시간")
    print("///////////////")
    print("")
    print(str(diff.days) + "days" + "   " + str(round(diff.seconds / 3600)) + "hours")
    print("")
    print("///////////////")


os.remove(SRC)
