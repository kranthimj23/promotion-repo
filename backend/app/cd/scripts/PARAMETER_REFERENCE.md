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
    --meta-sheet-repo <url> \
    --new-version <version> \
    --services-list <filepath> \
    --promotion-repo <url> \
    --target-branch <branch> \
    --promote-branch-x-1 <branch> \
    --promote-branch-x <branch> \
    --helmchart-repo <url>
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

---

## 🔀 Script-Specific Parameters

### Step 1: merger.py Parameters

#### `--meta-sheet-repo` (Required)
- **Input Type:** Repository URL (HTTPS)
- **Description:** Repository containing the meta-sheet.xlsx file
- **Expected file:** `meta-sheet.xlsx` on `master` branch
- **Example:** 
  ```
  --meta-sheet-repo https://github.com/kranthimj23/promotion-repo.git
  ```
- **Notes:** 
  - Must contain meta-sheet.xlsx with environment columns
  - Requires read/write access
  - Columns should match environment names (dev, sit, uat, prod)

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

#### `--promotion-repo` (Required)
- **Input Type:** Repository URL (HTTPS)
- **Description:** Repository where configuration values are promoted to
- **Expected structure:** 
  ```
  promotion-repo/
  ├── helm-charts/
  │   └── dev-values/
  │       └── app-values/
  └── ...
  ```
- **Example:** 
  ```
  --promotion-repo https://github.com/kranthimj23/mb-helmcharts.git
  ```
- **Notes:**
  - Typically the mb-helmcharts repository
  - Script will create necessary directories if they don't exist

#### `--target-branch` (Required)
- **Input Type:** Branch name
- **Description:** Target branch in promotion repository where values will be committed
- **Format:** Branch naming convention (e.g., `promotion-X.Y.Z`)
- **Example:** `--target-branch promotion-2.0.0`
- **Branch creation:** Script will create from `origin/main` if branch doesn't exist
- **Notes:**
  - Must match branch created by merger.py
  - Should follow naming convention for traceability

---

### Step 3: create-release-note.py Parameters

#### `--promote-branch-x-1` (Required)
- **Input Type:** Branch name
- **Description:** Branch representing the stable/previous release
- **Example:** `--promote-branch-x-1 promotion-1.0.0`
- **Used for:** Baseline comparison (older configuration)
- **Notes:**
  - Must exist in helmchart repository
  - Represents the "before" state

#### `--promote-branch-x` (Required)
- **Input Type:** Branch name
- **Description:** Branch representing the new/updated release
- **Example:** `--promote-branch-x promotion-2.0.0`
- **Used for:** New configuration (after values-promotion.py)
- **Notes:**
  - Should be the same as `--target-branch`
  - Represents the "after" state
  - Script will generate release notes comparing x-1 vs x

#### `--helmchart-repo` (Required)
- **Input Type:** Repository URL (HTTPS)
- **Description:** Repository containing the Helm charts for comparison
- **Expected structure:**
  ```
  helmchart-repo/
  ├── helm-charts/
  │   ├── dev-values/
  │   └── ... (other values)
  └── ... (chart definitions)
  ```
- **Example:** 
  ```
  --helmchart-repo https://github.com/kranthimj23/mb-helmcharts.git
  ```
- **Notes:**
  - Typically the same as `--promotion-repo`
  - Script clones both `--promote-branch-x-1` and `--promote-branch-x`

---

## 📊 Data Flow

```
User Input
    ↓
┌─────────────────────────────────────────┐
│ --lower-env, --higher-env               │
│ --meta-sheet-repo, --new-version        │
└─────────────┬───────────────────────────┘
              ↓
        [merger.py]
        Creates/finds branches
        Updates meta-sheet
              ↓
┌─────────────────────────────────────────┐
│ --services-list, --promotion-repo       │
│ --target-branch                         │
└─────────────┬───────────────────────────┘
              ↓
   [values-promotion.py]
   Collects configs from services
   Promotes to target-branch
              ↓
┌─────────────────────────────────────────┐
│ --promote-branch-x-1, --promote-branch-x│
│ --lower-env, --higher-env               │
│ --helmchart-repo                        │
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
    --meta-sheet-repo https://github.com/mycompany/meta-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --promotion-repo https://github.com/mycompany/mb-helmcharts.git \
    --target-branch promotion-2.0.0 \
    --promote-branch-x-1 promotion-1.9.5 \
    --promote-branch-x promotion-2.0.0 \
    --helmchart-repo https://github.com/mycompany/mb-helmcharts.git
```

### Example 2: SIT → UAT Promotion (Patch Version)
```bash
python main.py \
    --lower-env sit \
    --higher-env uat \
    --meta-sheet-repo https://github.com/mycompany/meta-repo.git \
    --new-version 2.0.1 \
    --services-list services_list.txt \
    --promotion-repo https://github.com/mycompany/mb-helmcharts.git \
    --target-branch promotion-2.0.1 \
    --promote-branch-x-1 promotion-2.0.0 \
    --promote-branch-x promotion-2.0.1 \
    --helmchart-repo https://github.com/mycompany/mb-helmcharts.git
```

### Example 3: UAT → PROD Promotion (Minor Version)
```bash
python main.py \
    --lower-env uat \
    --higher-env prod \
    --meta-sheet-repo https://github.com/mycompany/meta-repo.git \
    --new-version 2.1.0 \
    --services-list services_list.txt \
    --promotion-repo https://github.com/mycompany/mb-helmcharts.git \
    --target-branch promotion-2.1.0 \
    --promote-branch-x-1 promotion-2.0.1 \
    --promote-branch-x promotion-2.1.0 \
    --helmchart-repo https://github.com/mycompany/mb-helmcharts.git
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

1. **Parameter Order:** Parameters can be in any order (except as shown in template)
2. **Relative Paths:** Use relative paths from script directory or absolute paths
3. **URLs:** All GitHub URLs must be HTTPS format
4. **Branch Names:** Must exist (except target-branch which can be created)
5. **Environments:** Lower env must be "below" higher env in promotion hierarchy
6. **Versions:** Must follow semantic versioning (X.Y.Z)

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

