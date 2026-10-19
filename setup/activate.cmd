@echo off
rem Activates this PC with a licence key using the product's own Python (a fixed wrapper so the starter's SKILL.md can use one pre-approvable command).
rem usage: activate.cmd --key RSE-XXXXX-XXXXX-XXXXX-XXXXX [--replace]      (also: status | refresh | deactivate)
setlocal
if defined RSE_HOME ( set "HOMEDIR=%RSE_HOME%" ) else ( set "HOMEDIR=%USERPROFILE%\ReelsSinEditor" )
if not exist "%HOMEDIR%\venv\python.exe" ( echo ACTIVATE_FAILED: the private environment is not ready yet. Run first: cmd /c "%~dp0install.cmd" --env-only & exit /b 1 )
"%HOMEDIR%\venv\python.exe" -X utf8 "%~dp0activate.py" %*
exit /b %errorlevel%
