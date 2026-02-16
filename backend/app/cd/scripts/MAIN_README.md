# main.py - Master Orchestration Script

## 📌 Overview

`main.py` is a comprehensive orchestration script that automates the entire configuration promotion workflow by executing three scripts in sequence:

1. **merger.py** - Branch management and meta-sheet updates
2. **values-promotion.py** - Configuration value collection and promotion
3. **create-release-note.py** - Release note generation with change tracking

---

## 🚀 Quick Start

### 1. Create services_list.txt
```bash
cat > services_list.txt << 'EOF'
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
EOF
```

### 2. Set GitHub Token (Optional)
```bash
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Run Pipeline
```bash
python main.py \
    --lower-env dev \
    --higher-env sit \
    --promotional-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --target-branch promotion-2.0.0 \
    --promote-branch-x-1 promotion-1.0.0 \
    --promote-branch-x promotion-2.0.0
```

---

## 📚 Documentation Files

This directory now contains comprehensive documentation:

| File | Purpose |
|------|---------|
| **main.py** | Main orchestration script |
| **MAIN_ORCHESTRATION.md** | Detailed workflow and architecture |
| **MAIN_QUICKSTART.md** | Quick reference and examples |
| **PARAMETER_REFERENCE.md** | Complete parameter definitions |
| **COMMAND_BUILDER.md** | Interactive command building guide |

---

## 🔄 How It Works

### Pipeline Flow
```
Input Parameters
       ↓
┌──────────────────────────┐
│  Step 1: merger.py       │
│  ↳ Clone meta-sheet      │
│  ↳ Fetch branches        │
│  ↳ Create new branch     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────────┐
│  Step 2: values-promotion.py │
│  ↳ Read services list        │
│  ↳ Clone service repos       │
│  ↳ Extract configurations    │
│  ↳ Write to promotion repo   │
└────────────┬─────────────────┘
             ↓
┌──────────────────────────────────┐
│  Step 3: create-release-note.py  │
│  ↳ Compare branches              │
│  ↳ Generate Excel report         │
│  ↳ Create upgrade-services.txt   │
└────────────┬─────────────────────┘
             ↓
       Output Files
  (Release notes & logs)
```

---

## 📋 Required Parameters

### For All Scripts
- `--lower-env` - Source environment (dev, sit, uat)
- `--higher-env` - Target environment (sit, uat, prod)

### For merger.py
- `--meta-sheet-repo` - Repository with meta-sheet.xlsx
- `--new-version` - Version for new branch (X.Y.Z format)

### For values-promotion.py
- `--services-list` - File path with service URLs
- `--promotion-repo` - Helm charts repository
- `--target-branch` - Branch name for promotion

### For create-release-note.py
- `--promote-branch-x-1` - Stable release branch
- `--promote-branch-x` - Updated release branch
- `--helmchart-repo` - Helm charts repository for comparison

---

## 📊 Input/Output

### Input Requirements
```
services_list.txt
├── https://github.com/.../service-admin.git
├── https://github.com/.../service-user.git
└── https://github.com/.../service-auth.git
```

### Output Generated
```
promotion-repo/
├── release-note-2025-02-16-14-30-45.xlsx  ← Release notes
├── upgrade-services.txt                     ← Services to upgrade
└── helm-charts/
    └── dev-values/
        └── app-values/                      ← Promoted configs
```

---

## 🎯 Use Cases

### Use Case 1: Daily Development Promotion
```bash
python main.py \
    --lower-env dev \
    --higher-env sit \
    --meta-sheet-repo <repo> \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --promotion-repo <repo> \
    --target-branch promotion-2.0.0 \
    --promote-branch-x-1 promotion-1.9.0 \
    --promote-branch-x promotion-2.0.0 \
    --helmchart-repo <repo>
```

### Use Case 2: Release Candidate to UAT
```bash
python main.py \
    --lower-env sit \
    --higher-env uat \
    --meta-sheet-repo <repo> \
    --new-version 2.0.1 \
    --services-list services_list.txt \
    --promotion-repo <repo> \
    --target-branch promotion-2.0.1 \
    --promote-branch-x-1 promotion-2.0.0 \
    --promote-branch-x promotion-2.0.1 \
    --helmchart-repo <repo>
```

### Use Case 3: Production Release
```bash
python main.py \
    --lower-env uat \
    --higher-env prod \
    --meta-sheet-repo <repo> \
    --new-version 2.1.0 \
    --services-list services_list.txt \
    --promotion-repo <repo> \
    --target-branch promotion-2.1.0 \
    --promote-branch-x-1 promotion-2.0.1 \
    --promote-branch-x promotion-2.1.0 \
    --helmchart-repo <repo>
```

---

## 🔍 Command Reference

### Basic Command Structure
```bash
python main.py \
    [Global Options] \
    [merger.py Options] \
    [values-promotion.py Options] \
    [create-release-note.py Options]
```

### View Help
```bash
python main.py --help
```

### Dry Run (Check parameters)
```bash
# Just check if services_list.txt is readable
cat services_list.txt | wc -l
```

---

## ✅ Pre-Execution Checklist

- [ ] All GitHub URLs use HTTPS protocol
- [ ] `services_list.txt` file exists in same directory
- [ ] All service repositories are accessible
- [ ] Lower environment < Higher environment (in hierarchy)
- [ ] GIT_TOKEN environment variable is set (if needed)
- [ ] Branch names follow `promotion-X.Y.Z` convention
- [ ] New version follows semantic versioning
- [ ] All repository URLs are correct and accessible

---

## 📈 Expected Execution Timeline

| Stage | Time | Activity |
|-------|------|----------|
| Startup | 5s | Parameter validation |
| Step 1 (merger.py) | 2-3m | Clone meta-sheet, fetch branches |
| Step 2 (values-promotion.py) | 2-5m | Clone services, collect values |
| Step 3 (create-release-note.py) | 2-5m | Compare & generate reports |
| Cleanup | 1s | Final summary |
| **Total** | **5-15m** | Entire pipeline |

---

## 🛠️ Troubleshooting

### General Issues

**Issue:** "Services list file not found"
```bash
# Solution: Verify file exists
ls -la services_list.txt
```

**Issue:** "Git authentication failed"
```bash
# Solution: Set GIT_TOKEN
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Issue:** "Branch not found"
```bash
# Solution: Verify branch exists in repository
git ls-remote --heads <repo_url> <branch_name>
```

**Issue:** "Script not found"
```bash
# Solution: Verify location and file list
ls -la *.py | grep main.py
```

### Script-Specific Issues

For issues with individual scripts, see:
- `merger.py` - Check meta-sheet.xlsx format
- `values-promotion.py` - Check service repo structure
- `create-release-note.py` - Check helmchart directory layout

---

## 📞 Support & Documentation

### Quick References
- **MAIN_QUICKSTART.md** - Fast overview and examples
- **COMMAND_BUILDER.md** - Interactive command building guide
- **PARAMETER_REFERENCE.md** - Detailed parameter definitions

### Detailed Documentation
- **MAIN_ORCHESTRATION.md** - Complete workflow and architecture

### Individual Script Docs
- See README files in each script directory
- Check script headers for implementation details

---

## 🔐 Security Notes

1. **GitHub Token:** Store securely, never commit to version control
2. **SSH Keys:** Ensure agent is running for SSH repositories
3. **Repository Access:** User must have read/write permissions
4. **Credentials:** Use environment variables, not hardcoded values

---

## 🎓 Learning Path

1. Start with **MAIN_QUICKSTART.md** (5 min read)
2. Review **COMMAND_BUILDER.md** to build your command (10 min)
3. Study **PARAMETER_REFERENCE.md** for details (15 min)
4. Read **MAIN_ORCHESTRATION.md** for full understanding (30 min)
5. Run the pipeline with --help flag first
6. Execute with test repositories before production use

---

## 📝 Version History

- **v1.0** - Initial release with merger, values-promotion, and release-note orchestration

---

## 📄 License & Attribution

This orchestration script automates the execution of:
- `merger.py` - Branch management
- `values-promotion.py` - Configuration promotion
- `create-release-note.py` - Release documentation

All components work together to provide a complete configuration promotion pipeline.

---

## 🚀 Next Steps

1. Create `services_list.txt` with your service URLs
2. Review `MAIN_QUICKSTART.md` for a quick example
3. Use `COMMAND_BUILDER.md` to build your command
4. Execute the pipeline with your specific parameters
5. Monitor the output for success indicators (✅)

---

**Happy promoting! 🎉**



