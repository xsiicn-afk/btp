@echo off
chcp 65001 >nul

title ByTop Production Suite Builder

echo.
echo ===========================================
echo      ByTop Production Suite Builder
echo ===========================================
echo.

REM --------------------------------------------------
REM Проверяем виртуальное окружение
REM --------------------------------------------------

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo Не найдено виртуальное окружение .venv
    echo.
    pause
    exit /b
)

echo Проверка PyInstaller...

".\.venv\Scripts\python.exe" -m PyInstaller --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo PyInstaller не установлен.
    echo.
    echo Выполните:
    echo.
    echo .\.venv\Scripts\python.exe -m pip install pyinstaller
    echo.
    pause
    exit /b
)

echo.
echo Очистка старой сборки...

if exist build rmdir /S /Q build
if exist dist rmdir /S /Q dist
if exist "ByTop Production Suite.spec" del /Q "ByTop Production Suite.spec"

echo.
echo Сборка...

".\.venv\Scripts\python.exe" -m PyInstaller ^
    --clean ^
    --noconfirm ^
    --onedir ^
    --console ^
    --name "ByTop Production Suite" ^
    main.py

if errorlevel 1 (
    echo.
    echo Ошибка сборки.
    pause
    exit /b
)

echo.
echo Копирование ресурсов...

xcopy resources "dist\ByTop Production Suite\resources\" /E /I /Y >nul

echo.
echo Создание папки data...

if not exist "dist\ByTop Production Suite\data" (
    mkdir "dist\ByTop Production Suite\data"
)

echo.
echo Удаление тестовой базы...

#if exist "dist\ByTop Production Suite\data\bytop.db" (
#    del /Q "dist\ByTop Production Suite\data\bytop.db"
)

if exist "dist\ByTop Production Suite\data\serial_number.json" (
    del /Q "dist\ByTop Production Suite\data\serial_number.json"
)

echo.
echo ===========================================
echo Сборка успешно завершена.
echo ===========================================
echo.
echo Готовая программа:
echo.
echo dist\ByTop Production Suite
echo.

pause