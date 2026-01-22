@echo off
echo ==================================================
echo   ATTEMPTING LOCAL BUILD (REQUIRES FLUTTER)
echo ==================================================
echo.
echo 1. Installing Python Requirements...
pip install flet yt-dlp
echo.

echo 2. Checking for Flet/Flutter...
where flutter >nul 2>nul
if %errorlevel% neq 0 (
    color 0c
    echo [ERROR] Flutter SDK not found in PATH!
    echo.
    echo To build locally, you MUST have Flutter installed and configured.
    echo Since you don't have it, please use the GitHub Actions method (Cloud Build).
    echo.
    echo See HOW_TO_BUILD_APK.md for instructions.
    echo.
    pause
    exit /b
)

echo 3. Building APK...
echo This may take a while...
flet build apk

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo [ERROR] Build Failed.
    echo Verify your Android Studio SDK paths are correct.
    pause
) else (
    color 0a
    echo.
    echo [SUCCESS] APK created in 'build/apk' folder!
    pause
)
