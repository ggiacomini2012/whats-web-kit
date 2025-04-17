#!/bin/bash

echo "========================================"
echo " WhatsApp Bot Uninstaller Helper (macOS/Linux)"
echo "========================================"
echo
echo "This script will attempt to remove generated files and folders:"
echo "  - dist/"
echo "  - build/"
echo "  - gui.spec"
echo "  - bot.log"
echo "  - contact_log.json"
echo "  - __pycache__/"
echo "  - .venv/  (Virtual Environment - requires manual re-setup if needed again)"
echo
echo "WARNING: This action cannot be undone. Source code files"
echo "(like gui.py, bot.py, README.md, etc.) will NOT be deleted."
echo

read -p "Are you sure you want to proceed? (Y/N): " confirm
echo # Add a newline for cleaner output

if [[ "$confirm" != "Y" && "$confirm" != "y" ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo "Removing generated files and folders..."

# Use -f to force removal without confirmation prompts
rm -rf dist
rm -rf build
rm -f gui.spec
rm -f bot.log
rm -f contact_log.json
rm -rf __pycache__
rm -rf .venv

echo
echo "Cleanup attempt finished. Please check for any remaining files manually if needed." 