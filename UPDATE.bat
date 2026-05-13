@echo off
title Chess AI Coach - GitHub Update Tool
cd /d "%~dp0"

echo ========================================
echo    Chess AI Coach - GitHub Update Tool
echo ========================================
echo.

REM Check if git remote is configured
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo [FIRST TIME SETUP]
    echo.
    echo A GitHub repository must be created first.
    echo.
    echo Step 1: Go to https://github.com/new
    echo Step 2: Enter repository name: chess-ai-coach
    echo Step 3: Click "Create repository"
    echo Step 4: Copy the repository URL (e.g., https://github.com/YOUR-NAME/chess-ai-coach.git)
    echo.
    set /p url="Paste the GitHub URL: "
    if "%url%"=="" (
        echo No URL provided. Exiting.
        pause
        exit /b
    )
    git remote add origin %url%
    echo.
    echo Remote configured. Pushing to GitHub...
    echo.
    git push -u origin main
    if %errorlevel% equ 0 (
        echo.
        echo SUCCESS! Project published on GitHub.
    ) else (
        echo.
        echo ERROR: Push failed. Please check:
        echo  1. Did you create the repository on GitHub?
        echo  2. Is the URL correct?
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

echo Press Enter to commit and push (or Ctrl+C to cancel).
pause

git commit -m "Update %date% %time%"
git push

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! Changes pushed to GitHub.
) else (
    echo.
    echo ERROR: Push failed. Check your internet connection.
)

pause
