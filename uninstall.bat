@echo off
echo ========================================
echo  WhatsApp Bot Uninstaller Helper
echo ========================================
echo.
echo This script will attempt to remove generated files and folders:
echo   - dist/
echo   - build/
echo   - gui.spec
echo   - bot.log
echo   - contact_log.json
echo   - __pycache__/
echo   - .venv/  (Virtual Environment - requires manual re-setup if needed again)
echo.
echo WARNING: This action cannot be undone. Source code files
echo (like gui.py, bot.py, README.md, etc.) will NOT be deleted.
echo.

set /p "confirm=Are you sure you want to proceed? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Uninstall cancelled.
    goto :eof
)

echo Removing generated files and folders...

if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist gui.spec del /q gui.spec
if exist bot.log del /q bot.log
if exist contact_log.json del /q contact_log.json
if exist __pycache__ rmdir /s /q __pycache__
if exist .venv rmdir /s /q .venv

echo.
echo Cleanup attempt finished. Please check for any remaining files manually if needed.
pause
:eof 