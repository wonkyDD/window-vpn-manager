@echo off
echo.
echo.

for /f "delims=" %%i in ('mullvad account get') do (
    echo %%i
) >> temp.txt

python ..\src\expire.py

echo.
echo.
mullvad always-require-vpn set off
mullvad disconnect
echo.
echo.

:begin
for /f "delims=" %%i in ('mullvad status') do set output=%%i
if %output%==Disconnected goto end
echo Not Yet..
goto begin

:end
echo %output%

echo.
echo.
@REM Stop-Process -Name chrome
@REM 안전한 수단인 걸까? 위에 놈은 powershell에서는 되는데 batch에선 또 안됨


taskkill /F /IM chrome.exe /T

@REM %userprofile%/AppData/Local/Google/Chrome/Default/UserData/에서
@REM History 또는 History-journal을 주목.. Auto Wipe가 작동 안하는 이유?

@REM powershell에서는 되는데 batchfile에서는 안됨
@REM Set-Alias chrome "C:\Program Files\Google\Chrome\Application\chrome.exe"
@REM chrome --headless --print-to-pdf=d:\naver.pdf http://naver.com

python ..\end.py

echo.
echo.