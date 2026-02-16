# main.py - Visual Command Builder

## 🎯 Interactive Command Builder

Use this guide to build your command step-by-step.

---

## Step 1: Choose Your Promotion Path

### Option A: Dev → SIT
```
Lower Env: dev
Higher Env: sit
```

### Option B: SIT → UAT
```
Lower Env: sit
Higher Env: uat
```

### Option C: UAT → PROD
```
Lower Env: uat
Higher Env: prod
```

---

## Step 2: Define Your Repository

### Promotional Repository
- **Purpose:** Single repository for meta-sheet, promotion configs, and helmcharts
- **Format:** HTTPS GitHub URL
- **Example:** `https://github.com/kranthimj23/promotion-repo.git`
- **Your URL:** _________________

---

## Step 3: Define Your Versions and Branches

### New Version
- **Format:** Semantic versioning (X.Y.Z)
- **Example:** `2.0.0`, `2.0.1`, `2.1.0`
- **Your Version:** _________________

### Target Branch
- **Format:** `promotion-X.Y.Z`
- **Example:** `promotion-2.0.0`
- **Your Branch:** _________________

### Stable Release Branch
- **Purpose:** Previous/stable release for comparison
- **Format:** `promotion-X.Y.Z`
- **Example:** `promotion-1.9.5`
- **Your Branch:** _________________

### Updated Release Branch
- **Purpose:** New release for comparison (usually same as target branch)
- **Format:** `promotion-X.Y.Z`
- **Example:** `promotion-2.0.0`
- **Your Branch:** _________________

---

## Step 4: Create Services List

Create `services_list.txt` file:

```bash
cat > services_list.txt << EOF
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
https://github.com/kranthimj23/service-payment.git
EOF
```

### Services to Include
- [ ] service-admin
- [ ] service-user
- [ ] service-auth
- [ ] service-payment
- [ ] (add more as needed)

---

## Step 5: Build Your Command

### Template
```bash
python main.py \
    --lower-env {LOWER_ENV} \
    --higher-env {HIGHER_ENV} \
    --promotional-repo {PROMOTIONAL_REPO} \
    --new-version {VERSION} \
    --services-list services_list.txt \
    --target-branch {TARGET_BRANCH} \
    --promote-branch-x-1 {STABLE_BRANCH} \
    --promote-branch-x {UPDATED_BRANCH}
```

### Your Command
Copy and fill in the template above with your values:

```bash
python main.py \
    --lower-env {YOUR_LOWER_ENV} \
    --higher-env {YOUR_HIGHER_ENV} \
    --promotional-repo {YOUR_PROMOTIONAL_REPO} \
    --new-version {YOUR_VERSION} \
    --services-list services_list.txt \
    --target-branch {YOUR_TARGET_BRANCH} \
    --promote-branch-x-1 {YOUR_STABLE_BRANCH} \
    --promote-branch-x {YOUR_UPDATED_BRANCH}
```

---

## Pre-Execution Checklist

Before running your command:

- [ ] `services_list.txt` file exists with all service URLs
- [ ] All GitHub URLs are in HTTPS format
- [ ] All repositories are accessible (check network/VPN)
- [ ] Git token is set in environment (if needed): `export GIT_TOKEN=...`
- [ ] You have read/write access to the promotional repository
- [ ] Branch names follow the `promotion-X.Y.Z` convention
- [ ] Lower env is "below" higher env in promotion hierarchy
- [ ] `main.py` is in the `backend/app/cd/scripts/` directory

---

## Execution Steps

### 1. Navigate to Script Directory
```bash
cd backend/app/cd/scripts
```

### 2. Create Services List File
```bash
# Create or verify services_list.txt exists
ls -la services_list.txt
```

### 3. Set GitHub Token (Optional)
```bash
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Run the Command
```bash
python main.py \
    --lower-env dev \
    --higher-env sit \
    --promotional-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --target-branch promotion-2.0.0 \
    --promote-branch-x-1 promotion-1.9.5 \
    --promote-branch-x promotion-2.0.0
```

### 5. Monitor Output
- Wait for section headers (=== Signs ===)
- Look for ✅ (success) or ❌ (error) indicators
- Read error messages carefully if something fails

---

## Expected Output Timeline

```
[0s]   Pipeline Orchestration Started
       └─ Script directory validation

[5-30s] Step 1/3: Running merger.py
       └─ Clone promotional repo
       └─ Fetch branches
       └─ Create new branch if needed

[30s-5m] Step 2/3: Running values-promotion.py
        └─ Read services_list.txt
        └─ Clone each service repo
        └─ Extract dev-values
        └─ Write to promotional repo
        └─ Commit and push

[5m-15m] Step 3/3: Running create-release-note.py
        └─ Clone both promotion branches
        └─ Compare YAML configurations
        └─ Generate Excel report
        └─ Create upgrade-services.txt
        └─ Commit and push

[15m+] Pipeline Completed Successfully
```

---

## Quick Troubleshooting

| Error | Quick Fix |
|-------|-----------|
| "Services list file not found" | Run `ls services_list.txt` to verify |
| "Git authentication failed" | Check GIT_TOKEN: `echo $GIT_TOKEN` |
| "Branch not found" | Verify branch exists: `git branch -r` in repo |
| "Script not found" | Verify you're in correct directory |
| "Permission denied" | Check file permissions: `chmod +x main.py` |

---

## Common Variations

### Variation 1: Hotfix Release
```bash
# Release patch version for existing branch
--new-version 2.0.1
--promote-branch-x-1 promotion-2.0.0
--promote-branch-x promotion-2.0.1
```

### Variation 2: Minor Version Update
```bash
# Release minor version
--new-version 2.1.0
--promote-branch-x-1 promotion-2.0.0
--promote-branch-x promotion-2.1.0
```

### Variation 3: Major Version Update
```bash
# Release major version
--new-version 3.0.0
--promote-branch-x-1 promotion-2.0.0
--promote-branch-x promotion-3.0.0
```

---

## Notes

- **Run time:** Typically 5-15 minutes depending on number of services and repo sizes
- **Network:** Requires stable internet connection
- **Storage:** Temporary directories are created and cleaned up automatically
- **Logging:** All output is shown in real-time; consider redirecting to file for records

---

## Getting More Help

- See `MAIN_ORCHESTRATION.md` for detailed workflow
- See `PARAMETER_REFERENCE_NEW.md` for complete parameter definitions
- See `MAIN_QUICKSTART.md` for quick reference

