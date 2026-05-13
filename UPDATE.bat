@echo off
title Chess AI Coach - Update Tool
cd /d "%~dp0"

echo ========================================
echo    Chess AI Coach - GitHub Update Tool
echo ========================================
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Download from: https://git-scm.com/downloads
    pause
    exit /b
)

git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo [FIRST TIME SETUP]
    echo.
    echo Create a repository on GitHub:
    echo   Step 1: Go to https://github.com/new
    echo   Step 2: Repository name: chess-ai-coach
    echo   Step 3: Click "Create repository"
    echo.
    set /p url="Paste the GitHub URL: "
    if "%url%"=="" (
        echo No URL provided. Exiting.
        pause
        exit /b
    )
    git remote add origin %url%
    echo.
    git push -u origin main
    if %errorlevel% equ 0 (
        echo.
        echo SUCCESS! Project published on GitHub.
    ) else (
        echo.
        echo ERROR: Push failed. Make sure the URL is correct.
    )
    pause
    exit /b
)

echo Checking for changes...
git add -A

git diff --cached --stat --name-only > ._changes.txt
set has_changes=0
for %%a in (._changes.txt) do if %%~za gtr 0 set has_changes=1
del ._changes.txt 2>nul

if %has_changes% equ 0 (
    echo No changes detected. Everything is up to date.
    pause
    exit /b
)

echo.
echo Changes found:
git diff --cached --stat
echo.
echo Press Enter to commit and push (Ctrl+C to cancel).
pause

git commit -m "Update %date% %time%"
git push

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Changes pushed to GitHub.
) else (
    echo.
    echo Push failed. This is normal if you are not the repository owner.
    echo Only krsnaSuraj can push updates to this repo.
)

pause
