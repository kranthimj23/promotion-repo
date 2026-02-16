# ✅ main.py - Updated to Use sys.argv

## 🎉 Changes Made

The `main.py` script has been updated to use **direct sys.argv argument parsing** instead of argparse.

---

## 📋 Command Format

### Simple Positional Arguments (NO FLAGS NEEDED!)

```bash
python main.py <lower-env> <higher-env> <promotional-repo> <new-version> <services-list> <promote-branch-x-1>
```

### Example Command

```bash
python main.py dev sit https://github.com/kranthimj23/promotion-repo.git 2.0.0 services_list.txt release/1.0.0
```

---

## 📝 Argument Positions

| Position | Argument | Example |
|----------|----------|---------|
| **1** | lower-env | `dev` |
| **2** | higher-env | `sit` |
| **3** | promotional-repo | `https://github.com/kranthimj23/promotion-repo.git` |
| **4** | new-version | `2.0.0` |
| **5** | services-list | `services_list.txt` |
| **6** | promote-branch-x-1 | `release/1.0.0` |

---

## 🚀 Usage Examples

### Example 1: Dev → SIT
```bash
python main.py dev sit https://github.com/kranthimj23/promotion-repo.git 2.0.0 services_list.txt release/1.0.0
```

### Example 2: SIT → UAT
```bash
python main.py sit uat https://github.com/kranthimj23/promotion-repo.git 2.0.1 services_list.txt release/2.0.0
```

### Example 3: UAT → PROD
```bash
python main.py uat prod https://github.com/kranthimj23/promotion-repo.git 2.1.0 services_list.txt release/2.0.1
```

---

## 💡 What Happens Automatically

When you pass **new-version 2.0.0**, it auto-generates:
- `--target-branch` → `release/2.0.0`
- `--promote-branch-x` → `release/2.0.0`

No need to specify these anymore!

---

## 🔧 Quick Setup

### Step 1: Navigate to Scripts Directory
```bash
cd backend/app/cd/scripts
```

### Step 2: Create services_list.txt
```bash
cat > services_list.txt << EOF
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
EOF
```

### Step 3: Set GitHub Token (Optional)
```bash
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 4: Run the Pipeline
```bash
python main.py dev sit https://github.com/kranthimj23/promotion-repo.git 2.0.0 services_list.txt release/1.0.0
```

---

## ✅ Output

```
================================================================================
  Pipeline Orchestration Started
================================================================================

Script directory: /path/to/scripts

Parameters provided:
  Lower env: dev
  Higher env: sit
  Promotional repo: https://github.com/kranthimj23/promotion-repo.git
  New version: 2.0.0
  Services list: services_list.txt
  Promote branch x-1: release/1.0.0

Auto-generated branches from version 2.0.0:
  Target branch: release/2.0.0
  Promote branch-x: release/2.0.0

Services list file: services_list.txt
Found 3 services:
  1. https://github.com/kranthimj23/service-admin.git
  2. https://github.com/kranthimj23/service-user.git
  3. https://github.com/kranthimj23/service-auth.git

================================================================================
  Step 1/3: Running merger.py - Fetching branches and creating new branches if needed
================================================================================

Running: python merger.py dev sit https://github.com/kranthimj23/promotion-repo.git 2.0.0

✅ merger.py completed successfully.

================================================================================
  Step 2/3: Running values-promotion.py - Promoting configuration values
================================================================================

Running: python values-promotion.py services_list.txt https://github.com/kranthimj23/promotion-repo.git release/2.0.0

✅ values-promotion.py completed successfully.

================================================================================
  Step 3/3: Running create-release-note.py - Generating release notes
================================================================================

Running: python create-release-note.py release/1.0.0 release/2.0.0 dev sit https://github.com/kranthimj23/promotion-repo.git

✅ create-release-note.py completed successfully.

================================================================================
  Pipeline Completed Successfully
================================================================================

✅ All scripts executed successfully!

Summary:
  ✓ Merged branches using merger.py
  ✓ Promoted values using values-promotion.py
  ✓ Generated release notes using create-release-note.py
```

---

## 🆘 Help

If you run without arguments or with wrong number of arguments:

```bash
python main.py
```

Output:
```
❌ Error: Incorrect number of arguments!

Usage:
    python main.py <lower-env> <higher-env> <promotional-repo> <new-version> <services-list> <promote-branch-x-1>

Arguments:
    1. lower-env          : Source environment (dev, sit, uat)
    2. higher-env         : Target environment (sit, uat, prod)
    3. promotional-repo   : Promotion repository URL (HTTPS)
    4. new-version        : Version for release (X.Y.Z format)
    5. services-list      : Path to file with service URLs
    6. promote-branch-x-1 : Previous stable release branch (release/X.Y.Z)

Example:
    python main.py dev sit https://github.com/kranthimj23/promotion-repo.git 2.0.0 services_list.txt release/1.0.0

Auto-Generated:
    --target-branch → release/{new-version}
    --promote-branch-x → release/{new-version}
```

---

## 🎯 Key Benefits

✅ **Simple** - No flag names needed, just positional arguments
✅ **Clean** - Direct sys.argv parsing without argparse overhead
✅ **Fast** - Minimal overhead, quick startup
✅ **Clear** - Easy to understand what each argument does

---

**Ready to go!** 🚀

