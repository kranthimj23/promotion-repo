# values-promotion.py - Step-by-Step Execution Guide

## ✅ Prerequisites

- Python 3.6+ installed
- Git installed and in PATH
- Access to the repositories (public or with GIT_TOKEN)
- services_list.txt file with repository URLs

## 📋 Step-by-Step Instructions

### Step 1: Prepare Your services_list.txt

Create or edit `services_list.txt` in the root of your project:

```text
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
```

**Format rules:**
- One repository URL per line
- Empty lines are ignored
- Trailing/leading whitespace is trimmed
- No comments (lines starting with # are treated as URLs)

### Step 2: (Optional) Set GitHub Token

If your repositories are **private**, set the GIT_TOKEN:

**PowerShell:**
```powershell
$env:GIT_TOKEN = "ghp_your_personal_access_token_here"
```

**Command Prompt:**
```cmd
set GIT_TOKEN=ghp_your_personal_access_token_here
```

**Bash/Linux:**
```bash
export GIT_TOKEN="ghp_your_personal_access_token_here"
```

To get a token: https://github.com/settings/tokens

### Step 3: Run the Script

Execute the script with three arguments:

**PowerShell (recommended for Windows):**
```powershell
python .\backend\app\cd\scripts\values-promotion.py .\services_list.txt `
  https://github.com/your-org/promotion-repo.git dev2
```

**Command Prompt:**
```cmd
python .\backend\app\cd\scripts\values-promotion.py .\services_list.txt ^
  https://github.com/your-org/promotion-repo.git dev2
```

**Linux/Mac:**
```bash
python ./backend/app/cd/scripts/values-promotion.py ./services_list.txt \
  https://github.com/your-org/promotion-repo.git dev2
```

## 📊 Expected Output

```
Parsed 3 repositories from .\services_list.txt:
  - https://github.com/kranthimj23/service-admin.git
  - https://github.com/kranthimj23/service-user.git
  - https://github.com/kranthimj23/service-auth.git

Running: git clone --branch main https://github.com/kranthimj23/service-admin.git in C:\Users\...\tmpXXXX\service-admin
Source path: C:\...\service-admin\helm-charts\dev-values
Fetched 5 yaml files from https://github.com/kranthimj23/service-admin.git

...

Promotion repository updated successfully.
```

## 🔍 Verifying Success

1. **Check console output** for "Promotion repository updated successfully."
2. **Visit GitHub** and verify the promotion repo branch has new/updated YAML files
3. **Check commit history** in the target branch for recent commit

## ⚠️ Troubleshooting

### Error: Services list file not found
```
Error: Services list file '.services_list.txt' not found.
```
**Solution:** 
- Check file path spelling
- Verify services_list.txt exists in the directory
- Use full path if in different directory

### Error: No repositories found
```
Error: No repositories found in services list file.
```
**Solution:**
- Open services_list.txt and verify it has content
- Ensure each line has a valid repository URL
- Remove any comment lines (lines starting with #)

### Error: Git authentication failed
```
Failed to fetch from https://github.com/your-org/private-repo.git: ...
```
**Solution:**
- If private repo, set GIT_TOKEN: `$env:GIT_TOKEN = "your_token"`
- Verify token has access to the repository
- Check network connectivity

### Error: Branch not found
```
Error in prepare_promotion_repo: ... not found in repository
```
**Solution:**
- Verify target_branch name is correct
- Ensure promotion repo exists and is accessible
- Check branch exists in remote or will be created from main

## 📝 Complete Example (Copy-Paste Ready)

```powershell
# Windows PowerShell Full Example

# Step 1: Create services_list.txt (if not exists)
@"
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
"@ | Out-File -Encoding UTF8 services_list.txt

# Step 2: Set GitHub Token (if using private repos)
$env:GIT_TOKEN = "ghp_your_token_here"

# Step 3: Run the script
python .\backend\app\cd\scripts\values-promotion.py .\services_list.txt `
  https://github.com/your-org/promotion-repo.git dev2

# Step 4: Check result
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Script completed successfully!"
} else {
    Write-Host "❌ Script failed with exit code: $LASTEXITCODE"
}
```

## 🚀 Automation Example (Scheduled Task)

**PowerShell Script: run-values-promotion.ps1**
```powershell
# Set working directory
Set-Location "D:\test-data-generator-crn"

# Set token
$env:GIT_TOKEN = "ghp_your_token_here"

# Run the script
$result = python .\backend\app\cd\scripts\values-promotion.py .\services_list.txt `
  https://github.com/your-org/promotion-repo.git dev2

# Log result
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] Promotion completed. Exit code: $LASTEXITCODE" | `
  Add-Content ".\promotion-log.txt"

# Exit with same code as Python script
exit $LASTEXITCODE
```

## 📞 Need Help?

1. Check the **QUICK_REFERENCE.md** for common commands
2. Review **VALUES_PROMOTION_README.md** for detailed documentation
3. Check **REFACTORING_SUMMARY.md** for what changed
4. Verify services_list.txt format matches examples
5. Ensure GIT_TOKEN is set for private repositories

