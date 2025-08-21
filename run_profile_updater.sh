#!/bin/bash

# GitHub Profile Updater Launcher Script
# Makes it easy to run the profile updater with proper error handling

echo "🚀 GitHub Profile Updater"
echo "=========================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.6 or higher and try again"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.6"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old"
    echo "Please upgrade to Python 3.6 or higher"
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if required files exist
required_files=("github_profile_updater.py" "github_profile_config.json" "README.md")

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file not found: $file"
        echo "Please ensure all required files are in the current directory"
        exit 1
    fi
done

echo "✅ All required files found"

# Check if README.md is writable
if [ ! -w "README.md" ]; then
    echo "⚠️  Warning: README.md is not writable"
    echo "The updater will create README_UPDATED.md instead"
fi

# Run the profile updater
echo ""
echo "🔍 Starting project scan..."
echo "This may take a few minutes depending on your workspace size..."
echo ""

python3 github_profile_updater.py

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Profile update completed successfully!"
    echo ""
    echo "📁 Generated files:"
    if [ -f "README_UPDATED.md" ]; then
        echo "  - README_UPDATED.md (Your updated profile)"
    fi
    if [ -f "project_analysis.json" ]; then
        echo "  - project_analysis.json (Project analysis data)"
    fi
    echo ""
    echo "💡 Next steps:"
    echo "  1. Review README_UPDATED.md"
    echo "  2. Copy content to your GitHub profile README.md"
    echo "  3. Commit and push to GitHub"
    echo ""
else
    echo ""
    echo "❌ Profile update failed"
    echo "Check the error messages above for details"
    exit 1
fi