@echo off
REM GitHub Profile Updater Launcher Script for Windows
REM Makes it easy to run the profile updater with proper error handling

echo 🚀 GitHub Profile Updater
echo ==========================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.6 or higher and try again
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✅ Python %python_version% detected

REM Check if required files exist
if not exist "github_profile_updater.py" (
    echo ❌ Required file not found: github_profile_updater.py
    echo Please ensure all required files are in the current directory
    pause
    exit /b 1
)

if not exist "github_profile_config.json" (
    echo ❌ Required file not found: github_profile_config.json
    echo Please ensure all required files are in the current directory
    pause
    exit /b 1
)

if not exist "README.md" (
    echo ❌ Required file not found: README.md
    echo Please ensure all required files are in the current directory
    pause
    exit /b 1
)

echo ✅ All required files found

REM Check if README.md is writable
attrib -r "README.md" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Warning: README.md is read-only
    echo The updater will create README_UPDATED.md instead
)

REM Run the profile updater
echo.
echo 🔍 Starting project scan...
echo This may take a few minutes depending on your workspace size...
echo.

python github_profile_updater.py

REM Check if the script ran successfully
if %errorlevel% equ 0 (
    echo.
    echo 🎉 Profile update completed successfully!
    echo.
    echo 📁 Generated files:
    if exist "README_UPDATED.md" (
        echo   - README_UPDATED.md (Your updated profile)
    )
    if exist "project_analysis.json" (
        echo   - project_analysis.json (Project analysis data)
    )
    echo.
    echo 💡 Next steps:
    echo   1. Review README_UPDATED.md
    echo   2. Copy content to your GitHub profile README.md
    echo   3. Commit and push to GitHub
    echo.
) else (
    echo.
    echo ❌ Profile update failed
    echo Check the error messages above for details
    pause
    exit /b 1
)

pause