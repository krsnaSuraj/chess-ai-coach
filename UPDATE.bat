@echo off
title Chess AI Coach - Update Tool
cd /d "%~dp0"

echo ========================================
echo    Chess AI Coach - GitHub Update Tool
echo ========================================
echo.

REM Check if git remote is set
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo [FIRST TIME SETUP]
    echo.
    echo Pehle GitHub repository banana hoga.
    echo.
    echo Step 1: https://github.com/new  par jao
    echo Step 2: Repository name: chess-ai-coach  likho
    echo Step 3: "Create repository" button dabao
    echo Step 4: URL copy karo (dikhega: https://github.com/YOUR-NAME/chess-ai-coach.git)
    echo.
    set /p url="GitHub URL paste karo: "
    if "%url%"=="" (
        echo URL nahi diya. Script band.
        pause
        exit /b
    )
    git remote add origin %url%
    echo.
    echo Remote set ho gaya! Ab push kar rahe hain...
    echo.
    git push -u origin main
    if %errorlevel% equ 0 (
        echo.
        echo DONE! Project GitHub pe aa gaya.
    ) else (
        echo.
        echo ERROR: Push fail hua. Check karo:
        echo  1. GitHub pe repository bana li?
        echo  2. URL sahi hai?
    )
    pause
    exit /b
)

echo Changes check kar rahe hain...
git add -A

git diff --cached --stat --name-only > ._changes.txt
set has_changes=0
for %%a in (._changes.txt) do if %%~za gtr 0 set has_changes=1
del ._changes.txt 2>nul

if %has_changes% equ 0 (
    echo Koi change nahi hai. Sab up-to-date hai.
    pause
    exit /b
)

echo.
echo Changes found:
git diff --cached --stat
echo.

echo Commit ready hai. Enter dabao to push (ya Ctrl+C cancel karo).
pause

git commit -m "Update %date% %time%"
git push

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! GitHub pe update ho gaya.
) else (
    echo.
    echo ERROR: Push fail hua. Check internet connection.
)

pause
