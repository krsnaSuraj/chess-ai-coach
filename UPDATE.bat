@echo off
title Chess AI Coach - GitHub Update
cd /d "%~dp0"

echo ========================================
echo    Chess AI Coach - GitHub Update
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

if %has_changes% equ 0 (
    if "%unpushed%"=="0" (
        echo Everything up to date.
        pause
        exit /b
    )
    echo Pushing %unpushed% pending commit^(s^)...
    git push
    if %errorlevel% equ 0 ( echo SUCCESS! ) else ( echo FAILED. )
    pause
    exit /b
)

echo.
echo Changes to commit:
git diff --cached --stat
echo.
echo Press Enter to commit and push ^(Ctrl+C to cancel^)
pause

git commit -m "Update %date% %time%"
git push

if %errorlevel% equ 0 ( echo SUCCESS! ) else ( echo FAILED. )
pause
