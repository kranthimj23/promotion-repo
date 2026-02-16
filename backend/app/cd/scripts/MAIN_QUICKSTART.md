# Quick Start - main.py

## One-Liner Example

```bash
python main.py --lower-env dev --higher-env sit --promotional-repo https://github.com/kranthimj23/promotion-repo.git --new-version 2.0.0 --services-list services_list.txt --target-branch promotion-2.0.0 --promote-branch-x-1 promotion-1.0.0 --promote-branch-x promotion-2.0.0
```

## Parameters Summary

### 1️⃣ Merger.py Parameters
```
--lower-env dev                            (or sit, uat, etc.)
--higher-env sit                           (or uat, prod, etc.)
--promotional-repo <URL>                   (generic promotion repo)
--new-version 2.0.0                        (new version for branch creation)
```

### 2️⃣ Values-Promotion.py Parameters
```
--services-list services_list.txt          (file with service URLs)
--promotional-repo <URL>                   (generic promotion repo)
--target-branch promotion-2.0.0            (target branch name)
```

### 3️⃣ Create-Release-Note.py Parameters
```
--promote-branch-x-1 promotion-1.0.0       (stable release branch)
--promote-branch-x promotion-2.0.0         (updated release branch)
--lower-env dev                            (same as merger)
--higher-env sit                           (same as merger)
--promotional-repo <URL>                   (generic promotion repo)
```

## Setup Steps

### 1. Create services_list.txt
```bash
cat > services_list.txt << EOF
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
EOF
```

### 2. Set GitHub Token (Optional but Recommended)
```bash
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Run the Pipeline
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

## What Gets Executed

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: merger.py                                      │
│  ├─ Clone meta-sheet repo                               │
│  ├─ Fetch branches for dev and sit                       │
│  └─ Create new branch if needed                          │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Step 2: values-promotion.py                            │
│  ├─ Read services from services_list.txt                │
│  ├─ Clone each service repo                             │
│  ├─ Extract dev-values                                  │
│  ├─ Clone promotion repo                                │
│  ├─ Write values to target-branch                       │
│  └─ Commit and push                                     │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Step 3: create-release-note.py                         │
│  ├─ Clone mb-helmcharts (both branches)                │
│  ├─ Compare YAML files                                  │
│  ├─ Generate Excel release note                         │
│  ├─ Create upgrade-services.txt                         │
│  └─ Commit and push                                     │
└─────────────────────────────────────────────────────────┘
```

## Output

✅ **Success**: All three scripts complete successfully

❌ **Failure**: Pipeline stops at failing script

**Generated Files**:
- `release-note-<timestamp>.xlsx` - Release notes with detailed changes
- `upgrade-services.txt` - Services to upgrade with image tags
- Git commits to promotion and meta-sheet repositories

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Services list file not found" | Create services_list.txt or use absolute path |
| "Git authentication failed" | Set GIT_TOKEN environment variable |
| "Branch not found" | Verify branch names exist in repositories |
| "Script not found" | Run from backend/app/cd/scripts directory |

## Getting Help

See `MAIN_ORCHESTRATION.md` for detailed documentation.







