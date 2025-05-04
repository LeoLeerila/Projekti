@echo off
setlocal enabledelayedexpansion

echo Searching for mariadb.exe in Program Files...
set MARIADB_PATH=

for /d %%D in ("%ProgramFiles%\*") do (
    echo %%D | findstr /I "MariaDB" >nul
    if !errorlevel! == 0 (
        if exist "%%D\bin\mysql.exe" (
            set "MARIADB_PATH=%%D\bin\mysql.exe"
            goto :FOUND
        )
    )
)

:FOUND
if not defined MARIADB_PATH (
    echo Could not find mariadb.exe in Program Files
    pause
    exit /b 1
)

echo Found MariaDB at: %MARIADB_PATH%

REM Import SQL data
set "SQL_FILE=%~dp0projekti.sql"
echo Importing %SQL_FILE%...
"%MARIADB_PATH%" --host="127.0.0.1" --port=3306 --binary-mode=1 --user=pelaaja --password=pelaajansalasana flight_game_projekti < "%SQL_FILE%"

echo Database update done!
pause
