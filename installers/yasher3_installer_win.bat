@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    Установщик ящер3
echo ========================================
echo.

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Запуск без прав администратора. Установка в папку пользователя.
    set "TARGET=%LOCALAPPDATA%\Yascher3"
) else (
    echo Права администратора получены. Установка в Program Files.
    set "TARGET=%ProgramFiles%\Yascher3"
)

if not exist "!TARGET!" mkdir "!TARGET!"
echo Целевая папка: !TARGET!

echo Скачивание ящер3.exe...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/colddusssh/yasher3/raw/refs/heads/main/bin/ящер3.exe' -OutFile '!TARGET!\ящер3.exe' -UseBasicParsing"
if %errorlevel% neq 0 (
    echo Ошибка при скачивании!
    pause
    exit /b 1
)
echo Файл сохранён.

echo.
set /p ADD_PATH="Хотите добавить папку в PATH для текущего пользователя? (Y/N): "
if /i "!ADD_PATH!"=="Y" (
    :: Получаем текущий PATH пользователя
    for /f "tokens=2*" %%a in ('reg query HKCU\Environment /v PATH 2^>nul') do set "USER_PATH=%%b"
    if "!USER_PATH!"=="" (
        setx PATH "!TARGET!" >nul
    ) else (
        echo !USER_PATH! | find /i "!TARGET!" >nul
        if !errorlevel! equ 0 (
            echo Папка уже присутствует в PATH.
        ) else (
            setx PATH "!USER_PATH!;!TARGET!" >nul
        )
    )
    if !errorlevel! equ 0 (
        echo Папка добавлена в PATH (пользовательский)
    ) else (
        echo Ошибка при добавлении в PATH. Добавьте вручную:
        echo   1. Нажмите Win+R, введите sysdm.cpl
        echo   2. Переменные среды ^> PATH ^> Изменить
        echo   3. Добавьте строку: !TARGET!
    )
) else (
    echo Чтобы использовать ящер3 из командной строки, добавьте папку в PATH вручную:
    echo   !TARGET!
)

echo.
echo Установка завершена! Перезапустите командную строку.
pause