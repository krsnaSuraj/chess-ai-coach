@echo off
title Chess AI Coach - GitHub Update Tool
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
    echo Create a repository on GitHub first:
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
        echo SUCCESS! Project published on GitHub.
    ) else (
        echo ERROR: Push failed. Make sure the URL is correct.
    )
    pause
    exit /b
)

REM Check for unpushed commits
git log origin/main..HEAD --oneline > ._unpushed.txt 2>&1
set unpushed=0
for %%a in (._unpushed.txt) do if %%~za gtr 0 set unpushed=1

REM Check for unstaged changes
git add -A
git diff --cached --stat --name-only > ._changes.txt
set has_changes=0
for %%a in (._changes.txt) do if %%~za gtr 0 set has_changes=1

if %has_changes% equ 0 (
    if %unpushed% equ 0 (
        echo Everything is up to date. No changes to push.
        del ._unpushed.txt ._changes.txt 2>nul
        pause
        exit /b
    )
    echo.
    echo Found %unpushed% unpushed commit(s). Pushing to GitHub...
    echo.
    git push
    if %errorlevel% equ 0 (
        echo SUCCESS! Pushed to GitHub.
    ) else (
        echo ERROR: Push failed.
    )
    del ._unpushed.txt ._changes.txt 2>nul
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
    echo Push failed. This is expected if you are not the repository owner.
    echo Only the original maintainer can push updates to this repository.
)

del ._unpushed.txt ._changes.txt 2>nul
pause
