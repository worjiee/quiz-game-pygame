@echo off
echo =========================================
echo   Creating Executable for Mathify
echo =========================================
echo.
echo This will create a .exe file that your
echo friends can run WITHOUT installing Python!
echo.
pause

echo.
echo Step 1: Installing PyInstaller...
python -m pip install pyinstaller

echo.
echo Step 2: Creating executable...
echo This may take a few minutes...
pyinstaller --onefile --windowed --icon "mathifylogo.ico" --add-data "mathifylogo.png;." --add-data "music\\bg2.mp3;music" --add-data "music\\button1.mp3;music" --add-data "music\\correct.mp3;music" --add-data "music\\wrong.mp3;music" --name "Mathify" mathify_pygame.py

if %errorlevel%==0 (
    echo.
    echo =========================================
    echo   SUCCESS! Executable Created!
    echo =========================================
    echo.
    echo Your .exe file is in the "dist" folder
    echo File name: Mathify.exe
    echo.
    echo You can now:
    echo 1. Go to the "dist" folder
    echo 2. Copy Mathify.exe
    echo 3. Share it with your friends!
    echo.
    echo Friends can just double-click Mathify.exe
    echo No Python installation needed!
    echo.
) else (
    echo.
    echo =========================================
    echo   ERROR: Failed to create executable
    echo =========================================
    echo.
    echo Make sure Python 3.12 and Pygame are installed
    echo.
)

pause



