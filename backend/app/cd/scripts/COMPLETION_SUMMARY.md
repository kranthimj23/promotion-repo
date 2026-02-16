# ✅ Main.py Orchestration Script - COMPLETE

## 🎉 Summary

Successfully created a comprehensive orchestration script (`main.py`) that executes three scripts in sequence with a unified, generic `--promotional-repo` parameter for all operations.

---

## 📦 What Was Created

### Core Script
- **main.py** - Master orchestration script with full argument parsing and error handling

### Documentation Files
1. **MAIN_README.md** - Overview and quick start guide
2. **MAIN_QUICKSTART.md** - Quick reference with examples
3. **PARAMETER_REFERENCE_NEW.md** - Complete parameter definitions and data flow
4. **COMMAND_BUILDER.md** - Interactive command building guide

---

## 🔧 Architecture

### Single Repository Design
All three scripts now use ONE generic parameter: `--promotional-repo`

```
--promotional-repo https://github.com/kranthimj23/promotion-repo.git
                    ↓
                    ├─→ merger.py (reads meta-sheet.xlsx)
                    ├─→ values-promotion.py (promotes configs)
                    └─→ create-release-note.py (generates reports)
```

### Eliminated Redundancy
**Before:**
```
--meta-sheet-repo https://github.com/kranthimj23/promotion-repo.git
--promotion-repo https://github.com/kranthimj23/mb-helmcharts.git
--helmchart-repo https://github.com/kranthimj23/mb-helmcharts.git
```

**After:**
```
--promotional-repo https://github.com/kranthimj23/promotion-repo.git
```

---

## 📋 Command Structure

### Basic Template
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

### Parameters Overview

| Parameter | Used By | Purpose |
|-----------|---------|---------|
| `--lower-env` | All | Source environment (dev, sit, uat) |
| `--higher-env` | All | Target environment (sit, uat, prod) |
| `--promotional-repo` | All | Single repository for all operations |
| `--new-version` | merger.py | Version for new branch (X.Y.Z) |
| `--services-list` | values-promotion.py | File with service URLs |
| `--target-branch` | values-promotion.py | Target branch for promotion |
| `--promote-branch-x-1` | create-release-note.py | Stable release branch |
| `--promote-branch-x` | create-release-note.py | Updated release branch |

---

## 🚀 Pipeline Flow

```
INPUT: All Parameters + services_list.txt
    ↓
STEP 1: merger.py
    ├─ Clone promotional repo (master branch)
    ├─ Fetch current branches for lower/higher envs
    ├─ Create new branch if needed
    └─ Update meta-sheet.xlsx
    ↓
STEP 2: values-promotion.py
    ├─ Read services from services_list.txt
    ├─ Clone each service repository
    ├─ Extract dev-values from helm-charts
    ├─ Clone promotional repo
    ├─ Checkout/create target-branch
    ├─ Write values to app-values directory
    └─ Commit and push
    ↓
STEP 3: create-release-note.py
    ├─ Clone promotional repo (both branches)
    ├─ Compare YAML files
    ├─ Generate Excel release note
    ├─ Create upgrade-services.txt
    └─ Commit and push
    ↓
OUTPUT: 
    ├─ release-note-<timestamp>.xlsx
    ├─ upgrade-services.txt
    └─ Git commits in promotional repo
```

---

## 📄 Quick Start

### 1. Create services_list.txt
```bash
cat > services_list.txt << EOF
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
EOF
```

### 2. Set Environment (Optional)
```bash
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Run Pipeline
```bash
cd backend/app/cd/scripts

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

## 📊 File Manifest

```
backend/app/cd/scripts/
├── main.py                           ✅ NEW - Master orchestration script
├── MAIN_README.md                    ✅ NEW - Overview and quick start
├── MAIN_QUICKSTART.md                ✅ NEW - Quick reference guide
├── PARAMETER_REFERENCE_NEW.md        ✅ NEW - Complete parameter reference
├── COMMAND_BUILDER.md                ✅ NEW - Interactive command builder
├── merger.py                         (existing)
├── values-promotion.py               (existing)
├── create-release-note.py            (existing)
└── services_list.txt                 (user creates)
```

---

## 🎯 Key Features

### ✅ Single Repository Parameter
- One `--promotional-repo` URL for all three scripts
- Eliminates confusion and redundancy
- All repos point to the same place

### ✅ Comprehensive Documentation
- Multiple guides for different use cases
- Parameter reference with examples
- Interactive command builder
- Quick start and detailed workflows

### ✅ Error Handling
- Validates all required parameters
- Checks services_list.txt exists
- Verifies script files exist
- Stops execution on first failure

### ✅ User-Friendly Output
- Section headers for each step
- ✅ Success indicators
- ❌ Error messages
- Final summary

### ✅ Flexible Execution
- Parameters in any order
- Relative or absolute paths
- Optional GitHub token
- Graceful Ctrl+C handling

---

## 💡 Usage Examples

### Development → SIT
```bash
python main.py \
    --lower-env dev \
    --higher-env sit \
    --promotional-repo https://github.com/mycompany/promotion-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --target-branch promotion-2.0.0 \
    --promote-branch-x-1 promotion-1.9.0 \
    --promote-branch-x promotion-2.0.0
```

### SIT → UAT
```bash
python main.py \
    --lower-env sit \
    --higher-env uat \
    --promotional-repo https://github.com/mycompany/promotion-repo.git \
    --new-version 2.0.1 \
    --services-list services_list.txt \
    --target-branch promotion-2.0.1 \
    --promote-branch-x-1 promotion-2.0.0 \
    --promote-branch-x promotion-2.0.1
```

### UAT → PROD
```bash
python main.py \
    --lower-env uat \
    --higher-env prod \
    --promotional-repo https://github.com/mycompany/promotion-repo.git \
    --new-version 2.1.0 \
    --services-list services_list.txt \
    --target-branch promotion-2.1.0 \
    --promote-branch-x-1 promotion-2.0.1 \
    --promote-branch-x promotion-2.1.0
```

---

## 📝 Documentation Map

| Document | Best For |
|----------|----------|
| MAIN_README.md | Overview and quick start |
| MAIN_QUICKSTART.md | Fast command examples |
| PARAMETER_REFERENCE_NEW.md | Detailed parameter info |
| COMMAND_BUILDER.md | Interactive setup |

---

## ✨ Next Steps

1. ✅ Copy `services_list.txt` with your service URLs
2. ✅ Review `MAIN_QUICKSTART.md` for examples
3. ✅ Use `COMMAND_BUILDER.md` to build your command
4. ✅ Run the pipeline with `python main.py [arguments]`
5. ✅ Monitor output for ✅ success indicators

---

## 🔒 Security Notes

- Store GIT_TOKEN securely, never commit to version control
- Use HTTPS URLs for all repositories
- Ensure read/write permissions on promotional repo
- Use environment variables, not hardcoded credentials

---

## 🆘 Support

### Getting Help
- See MAIN_ORCHESTRATION.md for detailed workflow
- Check PARAMETER_REFERENCE_NEW.md for parameter definitions
- Review COMMAND_BUILDER.md for command setup

### Common Issues
- "Services list file not found" → Create services_list.txt in current directory
- "Git authentication failed" → Set GIT_TOKEN environment variable
- "Branch not found" → Verify branch exists in promotional repo
- "Script not found" → Run from backend/app/cd/scripts directory

---

## 🎉 You're Ready!

The main.py orchestration script is complete and ready to use. All three child scripts (merger.py, values-promotion.py, create-release-note.py) now work seamlessly with a single promotional repository parameter.

**Happy promoting!** 🚀

