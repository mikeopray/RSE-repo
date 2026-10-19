@echo off
rem Runs ONE of the product's own tools with the product's own Python, so a single fixed command can be pre-approved (Windows twin of rse.sh).
rem usage: rse.cmd engine\run_edit.py auto "<video>" --style signature-warm      (also setup\*.py)
setlocal
if defined RSE_HOME ( set "HOMEDIR=%RSE_HOME%" ) else ( set "HOMEDIR=%USERPROFILE%\ReelsSinEditor" )
set "T=%~1"
if "%T%"=="" ( echo RSE_USAGE: rse.cmd engine\^<tool^>.py [arguments] & exit /b 2 )
echo %T%| findstr /c:".." >nul && ( echo RSE_REFUSED: this wrapper only runs the product's own engine and setup tools. & exit /b 2 )
set "OK="
echo %T%| findstr /b /i /c:"engine\\" /c:"setup\\" >nul && set "OK=1"
if not defined OK ( echo RSE_REFUSED: this wrapper only runs the product's own engine and setup tools. & exit /b 2 )
if not exist "%HOMEDIR%\venv\python.exe" ( echo RSE_FAILED: the private environment is not ready. Run the setup again. & exit /b 1 )
set "ROOT=%~dp0..\"
shift
"%HOMEDIR%\venv\python.exe" -X utf8 "%ROOT%%T%" %*
exit /b %errorlevel%
