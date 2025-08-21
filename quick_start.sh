#!/bin/bash

# 🚀 GitHub Profile Updater - Quick Start Script
# This script helps you get started with the GitHub Profile Updater

echo "🚀 GitHub Profile Updater - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.6"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old. Please install Python 3.6 or higher."
    exit 1
fi

echo "✅ Python $python_version detected"
echo ""

# Check if required files exist
if [ ! -f "github_profile_updater.py" ]; then
    echo "❌ github_profile_updater.py not found in current directory"
    echo "Please run this script from the directory containing the updater files"
    exit 1
fi

if [ ! -f "github_profile_config.json" ]; then
    echo "❌ github_profile_config.json not found in current directory"
    echo "Please run this script from the directory containing the updater files"
    exit 1
fi

if [ ! -f "README.md" ]; then
    echo "⚠️  README.md not found. The system will use a default template."
    echo ""
fi

echo "✅ All required files found"
echo ""

# Show current configuration
echo "📋 Current Configuration:"
echo "------------------------"
base_path=$(python3 -c "import json; print(json.load(open('github_profile_config.json'))['scan_configuration']['base_path'])")
max_depth=$(python3 -c "import json; print(json.load(open('github_profile_config.json'))['scan_configuration']['max_depth'])")
echo "Base Path: $base_path"
echo "Max Depth: $max_depth"
echo ""

# Ask user to confirm
read -p "🚀 Ready to scan your workspace and update your GitHub profile? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting GitHub Profile Updater..."
    echo ""
    
    # Run the updater
    python3 github_profile_updater.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 Profile update completed successfully!"
        echo ""
        echo "📁 Generated files:"
        echo "  - README_UPDATED.md (your updated profile)"
        echo "  - project_analysis.json (detailed analysis)"
        echo "  - github_profile_updater.log (execution log)"
        echo ""
        echo "📝 Next steps:"
        echo "  1. Review README_UPDATED.md"
        echo "  2. Copy content to your README.md"
        echo "  3. Commit and push to GitHub"
        echo "  4. Run again weekly for updates!"
        echo ""
        echo "💡 Tip: You can customize the configuration in github_profile_config.json"
    else
        echo ""
        echo "❌ Profile update failed. Check the log file for details."
        exit 1
    fi
else
    echo "👋 Setup cancelled. You can run the updater manually with:"
    echo "   python3 github_profile_updater.py"
fi