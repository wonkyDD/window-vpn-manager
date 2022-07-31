import os
import sys
import subprocess


ps1_path = os.path.dirname(__file__) + '\\'
new_path = os.getcwd() + sys.argv[1][1:]

print(ps1_path)

tup = ('.', '#', '_', '@')
files = os.listdir(new_path)
files = filter(lambda f: not f.startswith(tup), files)


for f in files:
    p = subprocess.Popen(['powershell.exe',
                          ps1_path + '#github.ps1', 
                          new_path + f], stdout=subprocess.PIPE)
    
    out = p.communicate()[0]   
    result = out.decode('utf-8')
    s = result.split('\n')
    
    if s[0].startswith('origin\t'):
        link = s[0].lstrip('origin\t').rstrip('(fetch)')
        subprocess.Popen(['powershell.exe', f'Start-Process chrome {link}'])


    # TODO :
    # 1. git repo이름이 너무흔해서 내가 따로 이름을 지어버린 경우에 대한 에러처리
    else:
        if s[0].startswith('fatal:'):
            print(s[0])
            print(p.args + '내가 따로 이름을 지어버린 경우에 대해서 따로 처리해야합니다')
        
        else:
            print(s[0])
            print(p.args + f'{__file__} 에서 고려하지 못한 에러핸들링; 수정이 필요합니다')


subprocess.Popen(['powershell.exe', f'Set-Location -Path D:\\dev\\'])