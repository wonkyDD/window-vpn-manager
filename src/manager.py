import typer
# from _MULLVAD.locate import locate
from locate import locate
import os

# import subprocess

kor = typer.style(
    "KOREA로 파일을 이동",
    fg=typer.colors.BLUE,
)

chn = typer.style(
    ".CHINA로 파일을 이동",
    fg=typer.colors.RED,
)

mov = typer.style(
    ".MOVIE로 파일을 이동",
    fg=typer.colors.BLUE,
)

ACTION = ['FILE', 'MULLVAD']
GENRE = ['kor', 'chn', 'mov']

def main(
    action: str, 
    genre:  str     = typer.Option("","-g"), 
    detail: str     = typer.Option("","-d"), 
    formal: bool    = False
):
    is_valid_action = False
    for a in ACTION:
        if action.lower() == a.lower():
            is_valid_action = True
    
    if not is_valid_action:
        print("현재 내가 관리하는 action목록에 해당되지않음")
        raise typer.Exit()
    
    
    # TODO : How can I get terminal output
    # mullvad status가 connected가 된 후에 chrome start를 하는 방향
    if action.lower() == 'mullvad':
        if detail.lower() == 'on':
            os.system('..\script\mullvad_on.bat')
        
        if detail.lower() == 'off':
            os.system('..\script\mullvad_off.bat')
        
        # TODO : Reconnect하는 상황
        if detail.lower() == 're':
            pass
            
    
    if action.lower() == 'file':
        if not genre or not genre in GENRE:
            print("action이 file인 경우에는 genre가 명시되야하며, 명시됐을때에도 포함되는 장르인지 확인")
            raise typer.Exit()
        
        # TODO : 추후에 locate말고 다른 동작이 필요하다면?
        # if not detail:
        #     print("action이 file인 경우에는 file과 관련한 어떤 동작인지 detail이 요구됨")
        #     raise typer.Exit()
        
        
        if genre.lower() == 'kor':
            typer.echo(f"{kor}")
        
        if genre.lower() == 'chn':
            typer.echo(f"{chn}")
        
        if genre.lower() == 'mov':
            typer.echo(f"{mov}")
            
            
        # TODO : 추후에 locate말고 다른 동작이 필요하다면?
        locate(genre.lower())
    
    
if __name__ == "__main__":
    typer.run(main)