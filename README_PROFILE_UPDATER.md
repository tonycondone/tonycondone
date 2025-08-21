# 🚀 GitHub Profile Updater

A comprehensive Python-based system that automatically scans your development workspace for projects and generates an updated GitHub profile while preserving your existing aesthetic and animations.

## ✨ Features

- **🔍 Smart Project Discovery**: Automatically identifies development projects using multiple indicators
- **🛡️ Windows System Protection**: Ignores Windows system files and folders for safety
- **📊 Technology Analysis**: Extracts technologies, frameworks, and dependencies from project files
- **🎨 Profile Preservation**: Maintains your existing GitHub profile styling and animations
- **📈 Dynamic Updates**: Generates evidence-based skill assessments and project showcases
- **⚡ Performance Optimized**: Efficient scanning with configurable depth and exclusion rules

## 🏗️ System Architecture

### Core Components

1. **ProjectScanner**: Recursively scans file system for development projects
2. **ProfileGenerator**: Analyzes projects and generates updated profile content
3. **Configuration System**: Flexible JSON-based configuration for all scanning rules

### Project Detection

The system identifies development projects using multiple indicators:

- **Root Files**: `package.json`, `composer.json`, `requirements.txt`, `pom.xml`, etc.
- **Config Files**: `.gitignore`, `tsconfig.json`, `webpack.config.js`, etc.
- **Documentation**: `README.md`, `LICENSE`, `CHANGELOG.md`, etc.
- **Code Files**: `.py`, `.js`, `.php`, `.java`, `.html`, `.css`, etc.

### Technology Extraction

Automatically extracts technologies from:

- Package manager files (npm, composer, pip, maven, gradle, cargo, go)
- Import statements and dependencies
- Configuration files
- File content analysis

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.6 or higher
- Access to your development workspace
- Existing GitHub profile (README.md)

### 2. Installation

```bash
# Clone or download the files to your workspace
# Ensure you have these files:
# - github_profile_updater.py
# - github_profile_config.json
# - README.md (your current profile)
```

### 3. Configuration

Edit `github_profile_config.json` to customize:

- **Scan Path**: Set `base_path` to your development directory
- **Scan Depth**: Adjust `max_depth` for recursive scanning
- **Exclusion Rules**: Modify Windows system exclusions
- **Project Indicators**: Customize project detection patterns

### 4. Run the Updater

```bash
python3 github_profile_updater.py
```

### 5. Review Results

The system generates:
- `README_UPDATED.md` - Your updated profile
- `project_analysis.json` - Detailed project analysis

## ⚙️ Configuration Options

### Scan Configuration

```json
"scan_configuration": {
  "base_path": "/workspace",
  "recursive_scan": true,
  "max_depth": 5,
  "follow_symlinks": false
}
```

### Windows Exclusion Rules

The system automatically excludes:
- System folders (AppData, Desktop, Downloads, etc.)
- Windows application directories
- Temporary files and system files
- User profile directories

### Development Discovery Patterns

Customize what constitutes a development project:

```json
"project_indicators": {
  "root_files": ["package.json", "composer.json", "requirements.txt"],
  "config_files": [".gitignore", "tsconfig.json"],
  "documentation_files": ["README.md", "LICENSE"]
}
```

## 🔧 Customization

### Adding New Project Types

Extend the project classification system:

```json
"project_classification": {
  "new_category": {
    "indicators": ["specific_file", "technology_name"],
    "file_patterns": ["*pattern*", "*another*"]
  }
}
```

### Custom Technology Patterns

Add new technology detection patterns:

```json
"skill_extraction": {
  "from_file_content": {
    "new_tech": ["pattern1", "pattern2"]
  }
}
```

### Profile Template Customization

Modify the profile generation template:

```json
"profile_generation": {
  "current_profile_template": {
    "header": {
      "name": "Your Name",
      "roles": ["Your Roles"],
      "location": "Your Location"
    }
  }
}
```

## 📊 Output Sections

The updated profile includes:

1. **🌱 Current Focus**: Recent technologies and active projects
2. **🚀 Featured Projects**: Enhanced project showcase with discovered projects
3. **🛠️ Tech Stack**: Evidence-based technology badges and categories
4. **🏆 Recent Achievements**: Quantified accomplishments and metrics
5. **📊 Skills Matrix**: Skill proficiency levels based on project evidence
6. **📈 GitHub Stats**: Your existing GitHub statistics

## 🛡️ Safety Features

- **Privacy Protection**: Skips personal and sensitive files
- **System Safety**: Never scans Windows system directories
- **Permission Handling**: Gracefully handles inaccessible folders
- **File Size Limits**: Skips files larger than 10MB
- **Error Recovery**: Continues scanning even if individual projects fail

## 🔍 Project Analysis

Each discovered project is analyzed for:

- **Complexity Score**: Based on file count, code lines, and technology diversity
- **Technology Stack**: Extracted dependencies and frameworks
- **Project Type**: Automatic classification (web, data science, blockchain, etc.)
- **Recent Activity**: File modification timestamps
- **Documentation**: README content and project descriptions

## 📈 Skill Assessment

The system provides evidence-based skill levels:

- **🟢 Proficient**: 5+ projects or 100+ files
- **🟡 Intermediate**: 2-4 projects or 20-99 files
- **🔴 Beginner**: 1 project or 1-19 files

## 🎯 Use Cases

### For Developers
- Automatically update GitHub profiles with recent work
- Showcase diverse technology expertise
- Maintain professional appearance with minimal effort

### For Teams
- Standardize profile generation across team members
- Ensure consistent skill representation
- Track team technology adoption

### For Recruiters
- Evidence-based skill assessment
- Comprehensive project portfolio
- Technology stack transparency

## 🚨 Troubleshooting

### Common Issues

1. **No Projects Found**
   - Check `base_path` in configuration
   - Verify exclusion rules aren't too restrictive
   - Ensure projects have indicator files

2. **Permission Errors**
   - The system skips inaccessible folders automatically
   - Check folder permissions if needed

3. **Large File Warnings**
   - Files over 10MB are skipped for performance
   - This is normal and expected

### Debug Mode

Enable detailed logging by modifying the logging level in the script:

```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

## 🔄 Regular Updates

For best results, run the updater:

- **Weekly**: For active developers with frequent project changes
- **Monthly**: For developers with steady project development
- **Quarterly**: For developers with occasional project work

## 🤝 Contributing

The system is designed to be extensible. Common customization areas:

- New project type classifications
- Additional technology detection patterns
- Custom profile section generators
- Enhanced exclusion rules

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check the configuration file syntax
2. Verify Python version compatibility
3. Review the generated log output
4. Ensure your workspace structure is accessible

## 🎉 Success Stories

Users have successfully:
- Discovered 50+ hidden projects in their workspace
- Updated profiles with 20+ new technologies
- Showcased projects they forgot they built
- Improved their professional GitHub presence

---

**Ready to transform your GitHub profile?** 🚀

Run `python3 github_profile_updater.py` and watch your profile evolve with your actual development work!