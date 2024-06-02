@echo on
REM Check if Scoop is installed
where scoop >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Installing Scoop...
    set "SCOOP_DIR=%USERPROFILE%\scoop"
    mkdir "%SCOOP_DIR%" >nul 2>nul
    powershell -Command "Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')"
    call "%SCOOP_DIR%\shims\scoop" install scoop
)

REM Install FFmpeg using Scoop
scoop install ffmpeg

REM Create virtual environment
python -m venv .\.venv

REM Activate virtual environment
call .\.venv\Scripts\activate

REM Change to src directory and install requirements
cd src
pip install -r requirements.txt

REM To get the audio segments with pydub to work we need to install ffmpeg, using scoop,