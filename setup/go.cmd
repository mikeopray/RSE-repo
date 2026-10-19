@echo off
rem One-step setup for Windows: places this folder where Claude Code loads skills, prepares the private workspace, activates the licence key and installs everything else.
rem usage: go.cmd --key RSE-XXXXX-XXXXX-XXXXX-XXXXX [--replace]
rem It does exactly what the three separate steps did (install.cmd --env-only, activate.cmd --key, install.cmd), in one command. Safe to re-run.
setlocal
set "KEY="
set "MOVE="
:args
if "%~1"=="" goto :argsdone
if /i "%~1"=="--key" ( set "KEY=%~2" & shift & shift & goto :args )
if /i "%~1"=="--replace" ( set "MOVE=--replace" & shift & goto :args )
shift
goto :args
:argsdone
if "%KEY%"=="" ( echo SETUP_FAILED: I need the licence key from your purchase email ^(it looks like RSE-XXXXX-XXXXX-XXXXX-XXXXX^). & exit /b 1 )
set "SRC=%~dp0.."
set "DEST=%USERPROFILE%\.claude\skills\reels-sin-editor"
for %%i in ("%SRC%") do set "SRC=%%~fi"
if /i not "%SRC%"=="%DEST%" (
  if exist "%DEST%" (
    echo Reels Sin Editor is already in %DEST%: using it, nothing was replaced.
  ) else (
    if not exist "%USERPROFILE%\.claude\skills" mkdir "%USERPROFILE%\.claude\skills"
    xcopy "%SRC%" "%DEST%\" /E /I /Q /Y >nul
    if errorlevel 1 ( echo SETUP_FAILED: could not copy the product folder to %DEST%. & exit /b 1 )
    echo Copied the product folder to %DEST%
  )
)
if not exist "%DEST%\setup\install.cmd" ( echo SETUP_FAILED: %DEST% does not look like the Reels Sin Editor folder. Move it aside and run the setup again. & exit /b 1 )
call "%DEST%\setup\install.cmd" --env-only
if errorlevel 1 exit /b 1
call "%DEST%\setup\activate.cmd" --key "%KEY%" %MOVE%
if errorlevel 1 exit /b 1
call "%DEST%\setup\install.cmd"
exit /b %errorlevel%
