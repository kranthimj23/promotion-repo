# Main.py - Pipeline Orchestration Guide

## Overview
`main.py` is a master orchestration script that executes three scripts in sequence:
1. **merger.py** - Fetches branches from meta-sheet and creates new branches if needed
2. **values-promotion.py** - Promotes configuration values from service repos to promotion repo
3. **create-release-note.py** - Generates release notes comparing two promotion branches

## Prerequisites

### Environment Variables
Set the following environment variable before running:
```bash
# GitHub token for authentication (optional but recommended)
export GIT_TOKEN=<your_github_token>
```

### Required Files
- **services_list.txt** - File containing list of service repository URLs (one URL per line)

Example `services_list.txt`:
```
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
```

## Command Syntax

```bash
python main.py \
    --lower-env <env> \
    --higher-env <env> \
    --meta-sheet-repo <repo_url> \
    --new-version <version> \
    --services-list <file_path> \
    --promotion-repo <repo_url> \
    --target-branch <branch_name> \
    --promote-branch-x-1 <branch_name> \
    --promote-branch-x <branch_name> \
    --helmchart-repo <repo_url>
```

## Parameters

### Merger.py Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--lower-env` | Lower environment (source) | `dev` |
| `--higher-env` | Higher environment (target) | `sit` |
| `--meta-sheet-repo` | Repository containing meta-sheet.xlsx | `https://github.com/kranthimj23/promotion-repo.git` |
| `--new-version` | New version for branch creation | `2.0.0` |

### Values-Promotion.py Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--services-list` | Path to file with service repo URLs | `services_list.txt` |
| `--promotion-repo` | Promotion repository URL | `https://github.com/kranthimj23/mb-helmcharts.git` |
| `--target-branch` | Target branch for promotion | `promotion-2.0.0` |

### Create-Release-Note.py Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--promote-branch-x-1` | Stable release branch | `promotion-1.0.0` |
| `--promote-branch-x` | Updated release branch | `promotion-2.0.0` |
| `--lower-env` | Lower environment (same as merger) | `dev` |
| `--higher-env` | Higher environment (same as merger) | `sit` |
| `--helmchart-repo` | mb-helmcharts repository URL | `https://github.com/kranthimj23/mb-helmcharts.git` |

## Example Usage

### Development → SIT Promotion

```bash
python main.py \
    --lower-env dev \
    --higher-env sit \
    --meta-sheet-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --promotion-repo https://github.com/kranthimj23/mb-helmcharts.git \
    --target-branch promotion-2.0.0 \
    --promote-branch-x-1 promotion-1.9.0 \
    --promote-branch-x promotion-2.0.0 \
    --helmchart-repo https://github.com/kranthimj23/mb-helmcharts.git
```

### SIT → UAT Promotion

```bash
python main.py \
    --lower-env sit \
    --higher-env uat \
    --meta-sheet-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.1.0 \
    --services-list services_list.txt \
    --promotion-repo https://github.com/kranthimj23/mb-helmcharts.git \
    --target-branch promotion-2.1.0 \
    --promote-branch-x-1 promotion-2.0.0 \
    --promote-branch-x promotion-2.1.0 \
    --helmchart-repo https://github.com/kranthimj23/mb-helmcharts.git
```

## How It Works

### Step 1: Merger.py Execution
```
Input: lower_env, higher_env, meta_sheet_repo, new_version
Process:
  1. Clones meta-sheet repository from 'master' branch
  2. Fetches current branches for lower and higher environments
  3. If lower_env == 'dev' and lower_branch == higher_branch:
     - Creates new branch with new_version
     - Updates meta-sheet.xlsx
     - Commits and pushes to repository
Output: Updated meta-sheet with new branch entry
```

### Step 2: Values-Promotion.py Execution
```
Input: services_list, promotion_repo, target_branch
Process:
  1. Reads service repository URLs from services_list file
  2. For each service repository:
     - Clones the repository
     - Extracts dev-values from helm-charts directory
  3. Clones promotion repository
  4. Creates or checkouts target_branch
  5. Writes extracted values to promotion repo
  6. Commits and pushes changes to target_branch
Output: Updated promotion repository with latest configuration values
```

### Step 3: Create-Release-Note.py Execution
```
Input: promote_branch_x_1, promote_branch_x, lower_env, higher_env, helmchart_repo
Process:
  1. Clones mb-helmcharts from both promotion branches
  2. Compares YAML configurations between the two branches
  3. Identifies changes:
     - Added resources
     - Deleted resources
     - Modified configurations
  4. Generates Excel release note with detailed differences
  5. Creates upgrade-services.txt with image tag updates
  6. Commits and pushes release notes to target branch
Output: 
  - Release note Excel file (timestamp-based naming)
  - upgrade-services.txt with service upgrade information
```

## Output Files

### After Complete Pipeline Execution

1. **Excel Release Note** (in promotion repo)
   - Filename: `release-note-<timestamp>.xlsx`
   - Contains sheets for each environment
   - Details all changes between branches

2. **Upgrade Services File** (in promotion repo)
   - Filename: `upgrade-services.txt`
   - Lists services and their new image tags
   - Used for deployment automation

3. **Git Commits**
   - meta-sheet repository: "Add <new_branch> to meta-sheet"
   - promotion repository: "Sync dev-values from all services"
   - promotion repository: "Pushing the release_note into the branch: <target_branch>"

## Error Handling

The script will:
- ✅ Validate all required parameters
- ✅ Check that services_list file exists
- ✅ Verify each script exists before execution
- ✅ Stop execution if any script fails (exit code 1)
- ✅ Provide detailed error messages
- ✅ Support Ctrl+C interruption

## Logging and Output

The script provides:
- Section headers for each pipeline stage
- Command execution details
- Progress indicators (✅ for success, ❌ for errors)
- Final summary of execution

## Common Issues and Solutions

### Issue: "Services list file not found"
**Solution:** Ensure services_list.txt exists in the current directory or provide absolute path

### Issue: Git authentication errors
**Solution:** Set GIT_TOKEN environment variable with valid GitHub token
```bash
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Issue: Branch not found in meta-sheet
**Solution:** Verify that the lower_env and higher_env columns exist in meta-sheet.xlsx

### Issue: Promotion repo branch doesn't exist
**Solution:** The script will create the branch from 'origin/main' if it doesn't exist

## Stopping the Pipeline

Press **Ctrl+C** to interrupt at any time. The script will gracefully exit and report which stage was interrupted.

## Integration with CI/CD

The script can be integrated into Jenkins or GitLab CI:

```groovy
// Jenkins Example
stage('Promote Configuration') {
    steps {
        sh '''
            cd backend/app/cd/scripts
            python main.py \
                --lower-env ${LOWER_ENV} \
                --higher-env ${HIGHER_ENV} \
                --meta-sheet-repo ${META_SHEET_REPO} \
                --new-version ${NEW_VERSION} \
                --services-list services_list.txt \
                --promotion-repo ${PROMOTION_REPO} \
                --target-branch ${TARGET_BRANCH} \
                --promote-branch-x-1 ${STABLE_BRANCH} \
                --promote-branch-x ${RELEASE_BRANCH} \
                --helmchart-repo ${HELMCHART_REPO}
        '''
    }
}
```

## Performance Considerations

- **Total execution time:** 5-15 minutes (depending on repository sizes and network)
- **merger.py:** ~2-3 minutes
- **values-promotion.py:** ~2-5 minutes (scales with number of services)
- **create-release-note.py:** ~2-5 minutes

## Getting Help

For issues with individual scripts, check their respective README files:
- `merger.py` - Check git access, meta-sheet format
- `values-promotion.py` - Check service repos, branch availability
- `create-release-note.py` - Check helmchart repo, branch structure

