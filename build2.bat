@echo off
chcp 65001 > nul
title ByTop Production Suite - Build

echo =====================================
echo   ByTop Production Suite - Build
echo =====================================
echo.

REM Переход в папку скрипта
cd /d "%~dp0"

REM Активация виртуального окружения
if exist ".venv\Scripts\activate.bat" (
call ".venv\Scripts\activate.bat"
)

echo Проверка PyInstaller...
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
echo Установка PyInstaller...
pip install pyinstaller
)

echo.
echo Очистка старой сборки...
if exist build rmdir /S /Q build
if exist dist rmdir /S /Q dist
if exist "ByTop Production Suite.spec" del /Q "ByTop Production Suite.spec"

echo.
echo Сборка EXE...
python -m PyInstaller ^
--noconfirm ^
--clean ^
--onedir ^
--windowed ^
--name "ByTop Production Suite" ^
main.py

if errorlevel 1 (
echo.
echo =====================================
echo   ОШИБКА СБОРКИ
echo =====================================
pause
exit /b 1
)

echo.
echo Копирование ресурсов...

REM Шаблоны и иконки
if exist resources (
xcopy resources "dist\ByTop Production Suite\resources\" /E /I /Y
)

REM База данных
if exist database (
xcopy database "dist\ByTop Production Suite\database" /E /I /Y >nul
)

REM Данные программы (серийные номера и т.д.)
if exist data (
xcopy data "dist\ByTop Production Suite\data" /E /I /Y >nul
)

echo.
echo =====================================
echo   СБОРКА ЗАВЕРШЕНА
echo =====================================
echo.
echo Готовая папка:
echo dist\ByTop Production Suite
echo.
echo ВАЖНО:
echo - database\production.db сохранена
echo - data\serial_number.json сохранен
echo - resources\templates скопированы
echo.
pause
