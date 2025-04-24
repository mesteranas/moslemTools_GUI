@echo off
set "VENV_NAME=mtvenv"
if not exist "%VENV_NAME%\Scripts\activate.bat" (
    echo Virtual environment not found. Creating...
    python -m venv "%VENV_NAME%"
    call "%VENV_NAME%\Scripts\activate.bat"
    pip install -r requirements.txt
)

echo activating Virtual environment ...
cd moslemTools
start cmd /k "..\%VENV_NAME%\Scripts\activate.bat"