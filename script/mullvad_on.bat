@echo off
echo.
echo.

for /f "delims=" %%i in ('mullvad account get') do (
    echo %%i
) >> temp.txt

python ..\src\expire.py

echo.
echo.
mullvad always-require-vpn set on
mullvad connect


:begin
for /f "delims=" %%i in ('mullvad status') do set output=%%i

for %%i in (%output%) do (
    if %%i==Connected goto end

    echo Not Yet..
    goto begin
) 

:end
echo %output%


@REM start chrome 무조건 앞에 위치해야함
python ..\start.py


start chrome https://kissjav.li/videos/china-porn/ 
start chrome https://kissjav.li/videos/asian-porn-movies/ 
start chrome https://kissjav.li/videos/korean-bj/ 
start chrome https://kissjav.li/videos/korean-porn/ 
@REM start chrome chrome://downloads/




echo.
echo.
@REM start.py의 fetch가 담당함
@REM for /f "tokens=*" %%s in (..\remember.txt) do echo %%s
