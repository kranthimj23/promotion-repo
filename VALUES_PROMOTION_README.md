# values-promotion.py - Updated to Read Services List from File

## Overview
`values-promotion.py` has been rewritten to read the list of application repositories from a **file** instead of from an environment variable. This makes it easier to manage repository lists without setting environment variables.

## New Usage

```bash
python .\backend\app\cd\scripts\values-promotion.py <services_list_file> <promotion_repo> <target_branch>
```

### Arguments

1. **services_list_file** (required)
   - Path to a text file containing repository URLs (one per line)
   - Example: `services_list.txt`
   - File format:
     ```
     https://github.com/your-org/service-admin.git
     https://github.com/your-org/service-user.git
     https://github.com/your-org/service-auth.git
     ```

2. **promotion_repo** (required)
   - HTTPS Git repository URL for the promotion repository that will receive aggregated dev-values files
   - Example: `https://github.com/your-org/promotion-repo.git`
   - The script injects `GIT_TOKEN` (if set) for authenticated access

3. **target_branch** (required)
   - Target branch name in the promotion repository where files will be written and pushed
   - Example: `dev`, `dev2`, `feature/promotion-branch`
   - If the branch exists, it will be checked out; otherwise, it will be created from `origin/main`

## Environment Variables

- **GIT_TOKEN** (optional)
  - GitHub personal access token for private repositories
  - If set, the script automatically injects it into HTTPS URLs for authentication
  - Example: `$env:GIT_TOKEN = "your_token_here"`

## Example PowerShell Usage

```powershell
# Optional: Set GitHub token for private repos
$env:GIT_TOKEN = "ghp_your_personal_access_token"

# Run the script
python .\backend\app\cd\scripts\values-promotion.py .\services_list.txt `
  https://github.com/your-org/promotion-repo.git dev2
```

## File Format: services_list.txt

Create a plain text file with one repository URL per line:

```
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
```

- **Empty lines and whitespace** are automatically trimmed
- **Comments** are NOT supported (lines starting with `#` will be treated as URLs)
- Each URL must be a valid Git HTTPS repository URL

## What the Script Does

1. **Reads repositories** from the specified file
2. **Clones each service repository** on the `main` branch
3. **Collects YAML files** from `helm-charts/dev-values` in each repo
4. **Clones the promotion repository** and checks out the target branch
5. **Writes collected YAMLs** to `helm-charts/dev-values/app-values` in the promotion repo
6. **Commits and pushes** changes to the target branch with message: `"Sync dev-values from all services"`

## Error Handling

- If the services list file is not found, the script exits with error code 1
- If the file is empty or contains only whitespace, the script exits with error code 1
- If a repository cannot be cloned, the script logs the error and continues with the next repo
- Git authentication errors are reported but do not stop the process

## Changes from Previous Version

- **Old:** App repositories read from environment variable `app_repo_list`
- **New:** App repositories read from a file specified as the first argument
- **Benefit:** Easier to manage repository lists without needing to set environment variables

## Example services_list.txt

A sample `services_list.txt` is provided in the root directory of the project:

```
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
```

Feel free to modify this file to add, remove, or update repository URLs as needed.

