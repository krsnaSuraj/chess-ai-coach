@echo off
title Chess Coach - GitHub Update
cd /d "%~dp0"

echo ========================================
echo       Chess Coach - GitHub Update
echo ========================================
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git not found. Install from: https://git-scm.com/downloads
    pause
    exit /b
)

git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo First time setup:
    echo 1. Create repo on GitHub: https://github.com/new
    echo 2. Name: chess-ai-coach
    echo.
    set /p url="GitHub URL: "
    if "%url%"=="" exit /b
    git remote add origin %url%
    git push -u origin main
    if %errorlevel% equ 0 ( echo SUCCESS! ) else ( echo FAILED. )
    pause
    exit /b
)

git add -A
git diff --cached --quiet
set has_changes=%errorlevel%

for /f %%i in ('git rev-list --count origin/main..HEAD 2^>nul') do set unpushed=%%i

echo Current status:
for /f %%i in ('git rev-list --count HEAD 2^>nul') do set total=%%i
echo   Local commits: %total%
echo   Unpushed:      %unpushed%
echo   Uncommitted:   %has_changes% ^(0=clean, 1=changes^)
echo.

if %has_changes% equ 0 (
    if "%unpushed%"=="0" (
        echo Everything is up to date with GitHub.
        echo.
        echo Project URL: https://github.com/krsnaSuraj/chess-ai-coach
        pause
        exit /b
    )
    echo Found %unpushed% unpushed commit^(s^). Pushing...
    git push
    if %errorlevel% equ 0 ( echo SUCCESS! Pushed to GitHub. ) else ( echo FAILED. )
    pause
    exit /b
)

echo Changes found:
git diff --cached --stat
echo.
echo Press Enter to commit and push ^(Ctrl+C to cancel^)
pause

git commit -m "Update %date% %time%"
git push

if %errorlevel% equ 0 ( echo SUCCESS! ) else ( echo FAILED. )
pause
