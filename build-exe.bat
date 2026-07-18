@echo off
REM Build script for creating GW2TP Backend executable
echo Building GW2TP Backend executable...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
echo Installing dependencies...
pip install -r requirements-exe.txt

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

REM Build the executable
echo Building executable with PyInstaller...
pyinstaller backend.spec

REM Check if build was successful
if exist "dist\GW2TP_Python.exe" (
    echo.
    echo ===================================
    echo Build completed successfully!
    echo Executable location: dist\GW2TP_Python.exe
    echo ===================================
    echo.
    echo You can now distribute the contents of the 'dist' folder to users.
    echo Make sure to include any database files or configuration files needed.
) else (
    echo.
    echo ===================================
    echo Build failed! Check the output above for errors.
    echo ===================================
)

REM Copy to D:\GW2\addons\GW2TP
xcopy /E /I dist D:\GW2\addons\GW2TP

echo.
pause
