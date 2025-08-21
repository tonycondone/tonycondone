#!/usr/bin/env python3
"""
Test script for GitHub Profile Updater
Demonstrates the system functionality with sample data.
"""

import json
import os
from pathlib import Path
from github_profile_updater import ProjectScanner, ProfileGenerator

def create_sample_projects():
    """Create sample project directories for testing."""
    sample_projects = [
        {
            "name": "sample-python-app",
            "files": {
                "requirements.txt": "pandas\nnumpy\nmatplotlib\nscikit-learn",
                "main.py": "import pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import train_test_split",
                "README.md": "A Python data analysis application"
            }
        },
        {
            "name": "sample-php-project",
            "files": {
                "composer.json": '{"require": {"laravel/framework": "^10.0", "mysql": "^8.0"}}',
                "index.php": "<?php\nuse Laravel\\Framework\\Application;\nrequire_once 'vendor/autoload.php';",
                "README.md": "A Laravel-based web application"
            }
        },
        {
            "name": "sample-js-app",
            "files": {
                "package.json": '{"dependencies": {"react": "^18.0.0", "express": "^4.18.0"}}',
                "index.js": "import React from 'react';\nimport express from 'express';",
                "README.md": "A React + Express full-stack application"
            }
        }
    ]
    
    # Create test directory
    test_dir = Path("test_workspace")
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
    
    test_dir.mkdir()
    
    # Create sample projects
    for project in sample_projects:
        project_dir = test_dir / project["name"]
        project_dir.mkdir()
        
        for filename, content in project["files"].items():
            with open(project_dir / filename, 'w', encoding='utf-8') as f:
                f.write(content)
    
    return test_dir

def test_scanner():
    """Test the ProjectScanner functionality."""
    print("🧪 Testing ProjectScanner...")
    
    # Create sample projects
    test_dir = create_sample_projects()
    
    # Load configuration
    with open('github_profile_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Update config to use test directory
    config['github_profile_updater']['scan_configuration']['base_path'] = str(test_dir)
    
    # Initialize scanner
    scanner = ProjectScanner(config['github_profile_updater'])
    
    # Scan for projects
    projects = scanner.scan_projects(str(test_dir))
    
    print(f"✅ Found {len(projects)} projects:")
    for project in projects:
        print(f"  - {project['name']} ({project['type']})")
        print(f"    Technologies: {', '.join(project.get('technologies', [])[:5])}")
        print(f"    Complexity: {project.get('complexity_score', 0)}/100")
        print()
    
    return projects, config

def test_profile_generator(projects, config):
    """Test the ProfileGenerator functionality."""
    print("🧪 Testing ProfileGenerator...")
    
    # Initialize generator
    generator = ProfileGenerator(config['github_profile_updater'])
    
    # Create sample current profile
    current_profile = """# Sample Profile

## 🚀 Featured Project
Sample project description

## 🛠️ Tech Stack
Sample tech stack

## 🏆 Recent Achievements
Sample achievements

## 📊 GitHub Stats
Sample stats
"""
    
    # Generate updated profile
    updated_profile = generator.generate_profile(projects, current_profile)
    
    print("✅ Profile generation completed!")
    print(f"📝 Updated profile length: {len(updated_profile)} characters")
    
    # Save test output
    with open('test_output.md', 'w', encoding='utf-8') as f:
        f.write(updated_profile)
    
    print("💾 Test output saved to: test_output.md")
    
    return updated_profile

def cleanup_test_files():
    """Clean up test files."""
    test_files = [
        "test_workspace",
        "test_output.md"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            print(f"🧹 Cleaned up: {file_path}")

def main():
    """Main test function."""
    print("🚀 GitHub Profile Updater - Test Suite")
    print("=" * 50)
    
    try:
        # Test scanner
        projects, config = test_scanner()
        
        # Test profile generator
        updated_profile = test_profile_generator(projects, config)
        
        print("\n🎉 All tests completed successfully!")
        print("\n📊 Test Results:")
        print(f"  - Projects discovered: {len(projects)}")
        print(f"  - Profile updated: ✅")
        print(f"  - Output generated: test_output.md")
        
        # Show sample of discovered technologies
        all_techs = set()
        for project in projects:
            all_techs.update(project.get('technologies', []))
        
        print(f"  - Technologies found: {', '.join(sorted(all_techs)[:10])}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        print("\n🧹 Cleaning up test files...")
        cleanup_test_files()
        print("✅ Cleanup completed!")

if __name__ == "__main__":
    main()