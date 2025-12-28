@echo off
echo Setting up temporary environment...
set TEMP=C:\pg_temp
set TMP=C:\pg_temp
echo TEMP set to %TEMP%

echo Launching PostgreSQL installer...
"C:\Python\python_learn\pg_install.exe"

if %ERRORLEVEL% NEQ 0 (
    echo Installation failed or was cancelled. Error code: %ERRORLEVEL%
    pause
) else (
    echo Installer finished.
    pause
)
