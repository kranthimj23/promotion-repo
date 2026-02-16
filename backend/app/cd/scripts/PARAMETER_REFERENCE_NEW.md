# Complete Parameter Reference - main.py

## Script Execution Flow

```
main.py
├── merger.py (Step 1)
├── values-promotion.py (Step 2)
└── create-release-note.py (Step 3)
```

---

## 📋 Complete Command Template

```bash
python main.py \
    --lower-env <env1> \
    --higher-env <env2> \
    --promotional-repo <url> \
    --new-version <version> \
    --services-list <filepath> \
    --target-branch <branch> \
    --promote-branch-x-1 <branch> \
    --promote-branch-x <branch>
```

---

## 🔧 Parameter Definitions

### Global Parameters (Used by Multiple Scripts)

#### `--lower-env` (Required)
- **Used by:** merger.py, create-release-note.py
- **Type:** String
- **Valid values:** `dev`, `sit`, `uat`, `staging`, `prod`
- **Description:** Source environment for promotion
- **Example:** `--lower-env dev`

#### `--higher-env` (Required)
- **Used by:** merger.py, create-release-note.py
- **Type:** String
- **Valid values:** `sit`, `uat`, `staging`, `prod`
- **Description:** Target environment for promotion
- **Example:** `--higher-env sit`

#### `--promotional-repo` (Required)
- **Used by:** merger.py, values-promotion.py, create-release-note.py
- **Input Type:** Repository URL (HTTPS)
- **Description:** Generic promotion repository URL used for all operations
  - For merger.py: Repository containing the meta-sheet.xlsx file
  - For values-promotion.py: Repository where configuration values are promoted to
  - For create-release-note.py: Repository for helmchart comparison
- **Expected structure:** 
  ```
  promotional-repo/
  ├── meta-sheet.xlsx (for merger.py)
  ├── helm-charts/
  │   └── dev-values/
  │       └── app-values/ (for values-promotion.py)
  └── ... (chart definitions for create-release-note.py)
  ```
- **Example:** 
  ```
  --promotional-repo https://github.com/kranthimj23/promotion-repo.git
  ```
- **Notes:**
  - Single repository serves all three scripts
  - Must contain meta-sheet.xlsx on master branch
  - Requires read/write access
  - All necessary directories are created if they don't exist

---

## 🔀 Script-Specific Parameters

### Step 1: merger.py Parameters

#### `--new-version` (Required)
- **Input Type:** Version string (semantic versioning)
- **Description:** New version for branch creation
- **Format:** `X.Y.Z` (e.g., `2.0.0`, `1.5.1`)
- **Example:** `--new-version 2.0.0`
- **Used when:** lower_env is 'dev' and current branch equals higher_env branch
- **Notes:** 
  - If no new branch is needed, this may not be used
  - Must follow semantic versioning for consistency

---

### Step 2: values-promotion.py Parameters

#### `--services-list` (Required)
- **Input Type:** File path (relative or absolute)
- **Description:** Path to file containing service repository URLs
- **File format:** One GitHub URL per line (HTTPS)
- **File example:**
  ```
  https://github.com/kranthimj23/service-admin.git
  https://github.com/kranthimj23/service-user.git
  https://github.com/kranthimj23/service-auth.git
  https://github.com/kranthimj23/service-payment.git
  ```
- **Example:** `--services-list services_list.txt`
- **Notes:**
  - File must exist before execution
  - One URL per line (no empty lines between URLs)
  - All repos must contain `helm-charts/dev-values` directory structure
  - Blank lines and comments starting with # are ignored

#### `--target-branch` (Required)
- **Input Type:** Branch name
- **Description:** Target branch in promotion repository where values will be committed
- **Format:** Branch naming convention (e.g., `promotion-X.Y.Z`)
- **Example:** `--target-branch promotion-2.0.0`
- **Branch creation:** Script will create from `origin/main` if branch doesn't exist
- **Notes:**
  - Must match branch created by merger.py
  - Should follow naming convention for traceability
  - Script will checkout existing branch or create new one

---

### Step 3: create-release-note.py Parameters

#### `--promote-branch-x-1` (Required)
- **Input Type:** Branch name
- **Description:** Branch representing the stable/previous release
- **Example:** `--promote-branch-x-1 promotion-1.0.0`
- **Used for:** Baseline comparison (older configuration)
- **Notes:**
  - Must exist in promotion repository
  - Represents the "before" state
  - Should be an older or stable release

#### `--promote-branch-x` (Required)
- **Input Type:** Branch name
- **Description:** Branch representing the new/updated release
- **Example:** `--promote-branch-x promotion-2.0.0`
- **Used for:** New configuration (after values-promotion.py)
- **Notes:**
  - Should be the same as `--target-branch`
  - Represents the "after" state
  - Script will generate release notes comparing x-1 vs x

---

## 📊 Data Flow

```
User Input
    ↓
┌─────────────────────────────────────────┐
│ --lower-env, --higher-env               │
│ --promotional-repo, --new-version       │
└─────────────┬───────────────────────────┘
              ↓
        [merger.py]
        Creates/finds branches
        Updates meta-sheet
              ↓
┌─────────────────────────────────────────┐
│ --services-list                         │
│ --promotional-repo, --target-branch     │
└─────────────┬───────────────────────────┘
              ↓
   [values-promotion.py]
   Collects configs from services
   Promotes to target-branch
              ↓
┌─────────────────────────────────────────┐
│ --promote-branch-x-1, --promote-branch-x│
│ --lower-env, --higher-env               │
│ --promotional-repo                      │
└─────────────┬───────────────────────────┘
              ↓
  [create-release-note.py]
  Compares branches
  Generates Excel report
              ↓
        Output Files
   (release-note, upgrade-services.txt)
```

---

## 📝 Real-World Examples

### Example 1: Dev → SIT Promotion (New Version)
```bash
python main.py \
    --lower-env dev \
    --higher-env sit \
    --promotional-repo https://github.com/mycompany/promotion-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --target-branch promotion-2.0.0 \
    --promote-branch-x-1 promotion-1.9.5 \
    --promote-branch-x promotion-2.0.0
```

### Example 2: SIT → UAT Promotion (Patch Version)
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

### Example 3: UAT → PROD Promotion (Minor Version)
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

## 🔒 Environment Variables

### Required
None (all required parameters are command-line arguments)

### Optional but Recommended
```bash
# GitHub Personal Access Token (for authentication)
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Optional
```bash
# Python executable (if not using default)
export PYTHON_EXEC=python3.11
```

---

## ✅ Validation Rules

The script validates:

1. ✅ All required parameters are provided
2. ✅ `--services-list` file exists
3. ✅ All three script files exist in the same directory
4. ✅ Environment names are valid
5. ✅ URLs are properly formatted (HTTPS)

---

## 🚨 Error Scenarios

### Validation Errors
- Missing required parameter → Exit with usage message
- Services list file not found → Exit immediately
- Script files not found → Exit immediately

### Runtime Errors
- Git authentication failure → Stop at failing script
- Repository branch not found → Stop at failing script
- Directory permission issues → Stop at failing script

---

## 📌 Important Notes

1. **Single Repository:** All three scripts use the same `--promotional-repo` URL
2. **Parameter Order:** Parameters can be in any order
3. **Relative Paths:** Use relative paths from script directory or absolute paths
4. **URLs:** All GitHub URLs must be HTTPS format
5. **Branch Names:** Must exist (except target-branch which can be created)
6. **Environments:** Lower env must be "below" higher env in promotion hierarchy
7. **Versions:** Must follow semantic versioning (X.Y.Z)

---

## 🔄 Idempotency

- **merger.py:** Safe to run multiple times (checks existing entries)
- **values-promotion.py:** Overwrites existing files (not idempotent)
- **create-release-note.py:** Creates new timestamped files (safe to run multiple times)

---

## 📞 Support

For detailed information about individual scripts:
- See `merger.py` header comments for branch logic
- See `values-promotion.py` header comments for value collection
- See `create-release-note.py` header comments for comparison logic
- See `MAIN_ORCHESTRATION.md` for complete workflow documentation






