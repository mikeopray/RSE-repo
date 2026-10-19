@echo off
rem Reels Sin Editor installer for Windows 10 (1809+) / 11, 64-bit. Needs nothing from the user: no admin rights, no PowerShell settings, no Python/Node/ffmpeg to install first.
rem Step 1 (this file): a private Python 3.12, ffmpeg and Node in %USERPROFILE%\ReelsSinEditor\venv, made with micromamba (pinned and checksummed). Steps 2-6 run in the product's own Python (install_rest.py).
rem usage: install.cmd [--env-only]      Takes 10-20 minutes the first time (mostly downloads). Safe to re-run.
setlocal EnableDelayedExpansion
if defined RSE_HOME ( set "HOMEDIR=%RSE_HOME%" ) else ( set "HOMEDIR=%USERPROFILE%\ReelsSinEditor" )
set "VENV=%HOMEDIR%\venv"
set "TOOLS=%HOMEDIR%\tools"
set "HERE=%~dp0"
if /i "%PROCESSOR_ARCHITECTURE%"=="ARM64" goto :arm
if /i "%PROCESSOR_ARCHITEW6432%"=="ARM64" goto :arm
if not exist "%HOMEDIR%\projects" mkdir "%HOMEDIR%\projects"
if not exist "%HOMEDIR%\styles" mkdir "%HOMEDIR%\styles"
if not exist "%TOOLS%" mkdir "%TOOLS%"
set "MMVER=2.9.0-0"
set "MMSHA=a6d804394b2418991c4e29562853eaace2f2ce9d9da661a98e74e02e8dbb44b0"
set "MMDIR=%TOOLS%\mm-%MMVER%"
set "MM=%MMDIR%\micromamba.exe"
set "MAMBA_ROOT_PREFIX=%TOOLS%\mamba"
echo [1/6] Preparing Python 3.12, ffmpeg and Node (private copy, nothing is installed system-wide)...
set "READY=0"
if exist "%VENV%\python.exe" if exist "%VENV%\Library\bin\ffmpeg.exe" if exist "%VENV%\Library\bin\ffprobe.exe" set "READY=1"
if "%READY%"=="1" if not exist "%VENV%\node.exe" if not exist "%VENV%\Library\bin\node.exe" set "READY=0"
if "%READY%"=="0" (
  if not exist "%MM%" (
    if not exist "%MMDIR%" mkdir "%MMDIR%"
    curl.exe -fsSL --retry 3 -o "%MM%.part" "https://github.com/mamba-org/micromamba-releases/releases/download/%MMVER%/micromamba-win-64.exe"
    if errorlevel 1 goto :dlfail
    set "H="
    for /f "skip=1 tokens=*" %%h in ('certutil -hashfile "%MM%.part" SHA256') do if not defined H set "H=%%h"
    set "H=!H: =!"
    if /i not "!H!"=="%MMSHA%" ( del "%MM%.part" & goto :shafail )
    move /y "%MM%.part" "%MM%" >nul
  )
  if exist "%VENV%" rmdir /s /q "%VENV%"
  "%MM%" create -y -q -p "%VENV%" -c conda-forge --override-channels python=3.12 ffmpeg nodejs
  if errorlevel 1 goto :envfail
)
set "PATH=%VENV%;%VENV%\Scripts;%VENV%\Library\bin;%VENV%\Library\usr\bin;%VENV%\Library\mingw-w64\bin;%PATH%"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
if /i "%~1"=="--env-only" ( echo ENV_READY & exit /b 0 )
"%VENV%\python.exe" "%HERE%install_rest.py"
exit /b %errorlevel%
:arm
echo INSTALL_FAILED: this PC has an ARM processor. Reels Sin Editor does not support Windows on ARM yet (the speech-recognition engine has no version for it). It works on Windows PCs with Intel or AMD processors.
exit /b 1
:dlfail
echo INSTALL_FAILED: could not download the environment tool. Check the internet connection and run setup again.
exit /b 1
:shafail
echo INSTALL_FAILED: the downloaded environment tool did not match its checksum, so it was discarded for safety.
exit /b 1
:envfail
echo INSTALL_FAILED: could not create the environment. Check the internet connection and run setup again.
exit /b 1
