@echo off
chcp 65001 > nul

echo =====================================
echo   ByTop Production Suite - BUILD
echo =====================================

if not exist .venv (
echo [ОШИБКА] Не найдено виртуальное окружение .venv
pause
exit /b 1
)

call .venv\Scripts\activate.bat

echo.
echo [1/5] Проверка PyInstaller...
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
echo Устанавливаю PyInstaller...
pip install pyinstaller
)

echo.
echo [2/5] Очистка старой сборки...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ByTop.spec del /f /q ByTop.spec
if exist Release rmdir /s /q Release

echo.
echo [3/5] Сборка EXE...
python -m PyInstaller ^
--noconfirm ^
--clean ^
--windowed ^
--onedir ^
--name ByTop ^
main.py

if errorlevel 1 (
echo.
echo [ОШИБКА] Сборка не удалась
pause
exit /b 1
)

echo.
echo [4/5] Копирование ресурсов...
mkdir Release
xcopy dist\ByTop Release\ByTop\ /e /i /y
xcopy resources Release\ByTop\resources\ /e /i /y
xcopy database Release\ByTop\database\ /e /i /y
xcopy data Release\ByTop\data\ /e /i /y

echo.
echo [5/5] Готово
echo.
echo =====================================
echo   СБОРКА ЗАВЕРШЕНА
echo =====================================
echo.
echo Папка для тестирования:
echo Release\ByTop
echo.
pause
