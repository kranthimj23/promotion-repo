# values-promotion.py - Quick Reference

## Updated Command Syntax

```bash
python .\backend\app\cd\scripts\values-promotion.py <services_list_file> <promotion_repo> <target_branch>
```

## Arguments

| Argument # | Name | Type | Required | Example |
|-----------|------|------|----------|---------|
| 1 | services_list_file | File Path | Yes | `services_list.txt` |
| 2 | promotion_repo | Git URL | Yes | `https://github.com/org/promotion-repo.git` |
| 3 | target_branch | Branch Name | Yes | `dev` or `dev2` |

## Environment Variables

| Variable | Required | Default | Example |
|----------|----------|---------|---------|
| GIT_TOKEN | No | (none) | `ghp_xyz...` |

## File Format: services_list.txt

```
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
```

## Running the Script

### Step 1: Prepare services_list.txt
```bash
# Create or edit services_list.txt with your repository URLs
# One URL per line, no comments
```

### Step 2: (Optional) Set GitHub Token
```powershell
# For private repositories
$env:GIT_TOKEN = "your_personal_access_token"
```

### Step 3: Run the Script
```powershell
python .\backend\app\cd\scripts\values-promotion.py .\services_list.txt `
  https://github.com/your-org/promotion-repo.git dev2
```

## What the Script Does

1. ✓ Reads repository URLs from services_list.txt
2. ✓ Clones each service repository (main branch)
3. ✓ Collects YAML files from `helm-charts/dev-values`
4. ✓ Clones promotion repository
5. ✓ Writes YAML files to `helm-charts/dev-values/app-values`
6. ✓ Commits and pushes to target branch

## Output

```
Parsed 3 repositories from .\services_list.txt:
  - https://github.com/kranthimj23/service-admin.git
  - https://github.com/kranthimj23/service-user.git
  - https://github.com/kranthimj23/service-auth.git

Source path: ...
Fetched 5 yaml files from https://github.com/kranthimj23/service-admin.git

Verifying written files in promotion repo...
Found YAML: ...

Promotion repository updated successfully.
```

## Error Scenarios

| Error | Cause | Solution |
|-------|-------|----------|
| `Error: Services list file not found` | File path incorrect or doesn't exist | Create/verify services_list.txt path |
| `Error: No repositories found` | File is empty or contains only whitespace | Add repository URLs to services_list.txt |
| `Failed to fetch from <repo>` | Repository not accessible | Check URL, network, GIT_TOKEN |
| `Git command failed` | Authentication issue | Set GIT_TOKEN for private repos |
| `Error cloning promotion repo` | Promotion repo not found | Verify promotion_repo URL |

## Common Tasks

### Add a new service to promotion
```
1. Edit services_list.txt
2. Add new repository URL as a new line
3. Re-run the script
```

### Switch target branch
```powershell
python .\backend\app\cd\scripts\values-promotion.py .\services_list.txt `
  https://github.com/your-org/promotion-repo.git uat2
```

### Use private repositories
```powershell
$env:GIT_TOKEN = "ghp_xyz123..."
python .\backend\app\cd\scripts\values-promotion.py .\services_list.txt `
  https://github.com/your-org/promotion-repo.git dev
```

### Use different services list
```powershell
python .\backend\app\cd\scripts\values-promotion.py .\configs\staging-services.txt `
  https://github.com/your-org/promotion-repo.git staging
```

## More Information

- See `VALUES_PROMOTION_README.md` for detailed documentation
- See `REFACTORING_SUMMARY.md` for changes overview

