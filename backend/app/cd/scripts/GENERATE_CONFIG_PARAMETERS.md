# Generate-Config.py - Parameters Reference

## 📋 Overview

`generate-config.py` is a configuration generation script that:
1. Clones two branches from a promotion repository
2. Reads release notes from an Excel file
3. Applies configuration changes to YAML files
4. Generates updated configuration files
5. Commits and pushes changes back to the repository

---

## 🚀 Command Format

```bash
python generate-config.py <repo-url> <promote-branch-x-1> <promote-branch-x> <lower-env> <higher-env>
```

---

## 📝 Parameters (5 total)

### sys.argv[1] - promotional-repo (Repository URL)
- **Position:** 1st argument
- **Type:** String (HTTPS URL)
- **Description:** Promotion repository URL containing release notes and configuration files
- **Example:** `https://github.com/kranthimj23/promotion-repo.git`
- **Used for:** Cloning the repository with both branches

### sys.argv[2] - promote-branch-x-1 (Previous Release Branch)
- **Position:** 2nd argument
- **Type:** String (branch name)
- **Description:** Previous/stable release branch for baseline configuration
- **Example:** `release/1.0.0`
- **Used for:** Cloning as the baseline version
- **Format:** `release/X.Y.Z`

### sys.argv[3] - promote-branch-x (New Release Branch)
- **Position:** 3rd argument
- **Type:** String (branch name)
- **Description:** New/updated release branch with applied changes
- **Example:** `release/2.0.0`
- **Used for:** Main working branch where configs are generated
- **Format:** `release/X.Y.Z`

### sys.argv[4] - lower-env (Source Environment)
- **Position:** 4th argument
- **Type:** String
- **Valid values:** `dev`, `sit`, `uat`
- **Description:** Lower/source environment for configuration changes
- **Example:** `dev`
- **Used for:** Finding the correct sheet in release notes and mapping values

### sys.argv[5] - higher-env (Target Environment)
- **Position:** 5th argument
- **Type:** String
- **Valid values:** `sit`, `uat`, `prod`
- **Description:** Higher/target environment for configuration changes
- **Example:** `sit`
- **Used for:** Identifying which environment's values to promote

---

## 📊 Parameter Mapping

| Position | Variable | Type | Example | Description |
|----------|----------|------|---------|-------------|
| 1 | repo_url | URL | `https://github.com/.../promotion-repo.git` | Repository URL |
| 2 | promote_branch_x_1 | branch | `release/1.0.0` | Previous release |
| 3 | promote_branch_x | branch | `release/2.0.0` | New release |
| 4 | lower_env | env | `dev` | Source environment |
| 5 | higher_env | env | `sit` | Target environment |

---

## 💡 Real-World Examples

### Example 1: Dev → SIT Configuration Generation
```bash
python generate-config.py https://github.com/kranthimj23/promotion-repo.git release/1.0.0 release/2.0.0 dev sit
```

### Example 2: SIT → UAT Configuration Generation
```bash
python generate-config.py https://github.com/kranthimj23/promotion-repo.git release/2.0.0 release/2.0.1 sit uat
```

### Example 3: UAT → PROD Configuration Generation
```bash
python generate-config.py https://github.com/kranthimj23/promotion-repo.git release/2.0.1 release/2.1.0 uat prod
```

---

## 🔄 Workflow

```
Input Parameters
    ↓
Clone promote-branch-x-1 (baseline)
    ↓
Clone promote-branch-x (target)
    ↓
Find Release Note Excel File (marked as "verified")
    ↓
Read Configuration Changes from Excel
    ↓
Generate YAML Files with Changes
    ↓
Apply Changes to Deployment Configuration
    ↓
Commit and Push Changes
    ↓
Update Meta-Sheet
    ↓
Success
```

---

## 📂 Directory Structure Created

```
generate-config/
├── promotion-x-1/
│   └── promotion-repo/
│       └── helm-charts/
│           └── {lower-env}-values/
└── promotion-x/
    └── promotion-repo/
        └── helm-charts/
            └── {higher-env}-values/
                └── app-values/
                    ├── config-{env}.json
                    ├── {env}.txt
                    └── release_note/
                        └── release-note-VERIFIED.xlsx
```

---

## 📋 Expected Workflow

### What the Script Does

1. **Clones Two Branches**
   - `promote-branch-x-1` → baseline configuration
   - `promote-branch-x` → target configuration

2. **Reads Release Notes**
   - Finds Excel file with "verified" in filename
   - Extracts configuration changes for `higher-env`

3. **Generates Configurations**
   - Reads YAML files from baseline
   - Applies changes from Excel (add/modify/delete)
   - Creates updated JSON files

4. **Updates Helm Charts**
   - Modifies deployment.yaml for deleted services
   - Inserts hardcoded values for new services
   - Creates YAML files from updated JSON

5. **Commits Changes**
   - Stages all changes
   - Commits with message: `Config files generated: {promote-branch-x}`
   - Pushes to origin

6. **Updates Meta-Sheet**
   - Updates meta-sheet.xlsx to mark promotion as complete

---

## ✅ Prerequisites

1. **GIT_TOKEN** environment variable set (optional but recommended)
   ```bash
   export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

2. **Release Note File**
   - Must exist in: `promotion-x/helm-charts/{higher-env}-values/app-values/release_note/`
   - Must have "verified" in filename
   - Example: `release-note-DEV-to-SIT-verified.xlsx`

3. **Excel File Columns**
   - Service name
   - Change Request (add/modify/delete)
   - Key (path to configuration)
   - Comment
   - `{lower-env}-current value`
   - `{lower-env}-previous value`
   - `{higher-env}-current value`
   - `{higher-env}-previous value`

---

## 🔍 Verification

Before running, ensure:

```bash
# 1. Repository URL is correct
git clone --depth 1 https://github.com/kranthimj23/promotion-repo.git test-repo

# 2. Branches exist
git branch -r | grep release/

# 3. Release note exists
ls -la promotion-x/helm-charts/sit-values/app-values/release_note/

# 4. GIT_TOKEN is set (if needed)
echo $GIT_TOKEN
```

---

## ⚠️ Important Notes

1. **Branch Names:** Must follow `release/X.Y.Z` format
2. **Environment Hierarchy:** Lower env must be "below" higher env
3. **Release Note:** Must have "verified" in filename
4. **Git User:** Script uses hardcoded git user (kranthimj23@gmail.com)
5. **Working Directory:** Script creates `generate-config/` folder in current directory

---

## 🆘 Common Errors

### Error: "Release note does not exist"
**Cause:** Excel file with "verified" not found in expected path
**Solution:** Generate release notes using `create-release-note.py` first

### Error: "Git command failed"
**Cause:** Network or authentication issue
**Solution:** Check GIT_TOKEN and repository access

### Error: "Environment not found in header"
**Cause:** Column name mismatch in Excel
**Solution:** Verify Excel has correct environment columns (e.g., `dev-current value`, `sit-current value`)

---

## 📝 Output Files

After successful execution:

1. **Configuration Files**
   - `config-{env}.json` - Updated configuration in JSON format
   - `{env}-values/app-values/*.yaml` - YAML configuration files

2. **Service List**
   - `{env}.txt` - List of services to be deployed

3. **Git Commits**
   - Message: `Config files generated: {promote-branch-x}`
   - Meta-sheet updates

---

## 🚀 Ready to Use

**Copy and customize this command:**

```bash
python generate-config.py https://github.com/kranthimj23/promotion-repo.git release/1.0.0 release/2.0.0 dev sit
```

**Replace values:**
- `release/1.0.0` → Your previous release branch
- `release/2.0.0` → Your new release branch
- `dev` → Your source environment
- `sit` → Your target environment

