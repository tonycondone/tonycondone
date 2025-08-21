# 🚀 GitHub Profile Updater - Quick Start Guide

## ⚡ Get Started in 3 Steps

### 1. 🎯 Update Configuration
Edit `github_profile_config.json` and change:
```json
"scan_configuration": {
  "base_path": "C:\\Users\\Admin\\Documents\\Projects"  // Your dev directory
}
```

### 2. 🚀 Run the Updater

**Windows:**
```cmd
run_profile_updater.bat
```

**Linux/macOS:**
```bash
chmod +x run_profile_updater.sh
./run_profile_updater.sh
```

**Manual:**
```bash
python3 github_profile_updater.py
```

### 3. 📝 Update Your Profile
- Review `README_UPDATED.md`
- Copy content to your GitHub profile README.md
- Commit and push to GitHub

## 📁 What You Get

- **`README_UPDATED.md`** - Your enhanced profile
- **`project_analysis.json`** - Project analysis data
- **Automated discovery** of 10-50+ projects
- **Evidence-based skills** from actual code
- **Professional portfolio** showcase

## 🔧 Customization

- **Scan Path**: Change `base_path` in config
- **Scan Depth**: Adjust `max_depth` (default: 5)
- **Exclusions**: Modify Windows system exclusions
- **Project Types**: Add new classification rules

## 🛡️ Safety Features

- ✅ Never scans Windows system files
- ✅ Skips personal/sensitive data
- ✅ Handles permissions gracefully
- ✅ Limits file size for performance

## 🧪 Test First

Verify the system works:
```bash
python3 test_profile_updater.py
```

## 📞 Need Help?

- **Documentation**: `README_PROFILE_UPDATER.md`
- **Complete Guide**: `SYSTEM_SUMMARY.md`
- **Configuration**: `github_profile_config.json`

---

**🎉 Ready to transform your GitHub profile? Run the updater now!**