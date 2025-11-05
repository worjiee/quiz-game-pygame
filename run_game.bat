@echo off
echo Starting Mathify...
echo.

REM Try Python 3.12 first (needed for Pygame)
py -3.12 mathify_pygame.py 2>nul
if %errorlevel%==0 goto end

REM If that fails, try regular python
python mathify_pygame.py 2>nul
if %errorlevel%==0 goto end

REM If still fails, show error
echo.
echo ERROR: Pygame not installed or Python 3.12 not found!
echo.
echo Python 3.14 is too new for Pygame.
echo Please install Python 3.12 - see PYTHON_INSTALL_GUIDE.md
echo.
echo Download Python 3.12 from: https://www.python.org/downloads/
echo.

:end
pause

