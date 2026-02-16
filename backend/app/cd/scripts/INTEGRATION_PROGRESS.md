# Git Helpers Integration Guide

## ✅ Integration Complete for promotion_branch_manager.py

The `promotion_branch_manager.py` script has been successfully updated to use `git_helpers` functions.

---

## 🔄 Changes Made to promotion_branch_manager.py

### 1. Added Import
```python
from git_helpers import clone_single_branch_and_checkout, configure_git_user, stage_specific_files_commit_and_push
```

### 2. Removed Functions
- ❌ `clone_repo_master()` - Replaced with `git_helpers.clone_single_branch_and_checkout()`

### 3. Updated Code

#### Before:
```python
clone_repo_master(github_url, "master", target_folder)

# Later in create_github_branch:
subprocess.run(['git', 'config', 'user.email', 'kranthimj23@gmail.com'], cwd=master_dir, check=True)
subprocess.run(['git', 'config', 'user.name', 'kranthimj23'], cwd=master_dir, check=True)
subprocess.run(['git', 'add', 'meta-sheet.xlsx'], cwd=master_dir, check=True)
subprocess.run(['git', 'commit', '-m', f'Add {new_branch} to meta-sheet'], cwd=master_dir, check=True)
subprocess.run(['git', 'push', 'origin', 'master'], cwd=master_dir, check=True)
```

#### After:
```python
clone_single_branch_and_checkout(github_url, "master", target_folder)

# Later in create_github_branch:
configure_git_user(master_dir)
stage_specific_files_commit_and_push(
    master_dir,
    "master",
    f'Add {new_branch} to meta-sheet',
    ["meta-sheet.xlsx"],
    pull_before_push=False
)
```

---

## 📊 Code Reduction

- **Lines Removed:** ~35 lines of duplicated git code
- **Improved Readability:** More declarative, clearer intent
- **Better Maintainability:** Git operations now centralized

---

## 🎯 Remaining Scripts to Integrate

### High Priority (Most duplication)
- [ ] **values-promotion.py** - Multiple git clone/commit/push operations
- [ ] **create-release-note.py** - Extensive git operations
- [ ] **generate-config.py** - Clone and commit operations

### Medium Priority
- [ ] **script.py** - Git operations for config generation
- [ ] **app_db_infra_pull_services.py** - Git clone operations

### Infrastructure Scripts
- [ ] Backend DB CD/CI scripts
- [ ] Backend Infra CD/CI scripts

---

## 🚀 Integration Roadmap

### Phase 1: Core Scripts ✅ DONE
- [x] promotion_branch_manager.py

### Phase 2: Application Promotion (Next)
- [ ] values-promotion.py
- [ ] create-release-note.py

### Phase 3: Configuration
- [ ] generate-config.py
- [ ] script.py

### Phase 4: Infrastructure
- [ ] app_db_infra_pull_services.py
- [ ] Backend/infra scripts

---

## ✨ Benefits Achieved in promotion_branch_manager.py

✅ Eliminated `clone_repo_master()` function
✅ Using centralized `clone_single_branch_and_checkout()`
✅ Using centralized `configure_git_user()`
✅ Using centralized `stage_specific_files_commit_and_push()`
✅ ~35 lines of duplicated code removed
✅ Consistent git configuration across the script

---

## 📋 Testing Checklist

Before deploying, verify:

```bash
# 1. Test clone operation
python promotion_branch_manager.py dev sit https://repo.git 2.0.0

# 2. Verify branch creation works
# 3. Check meta-sheet.xlsx was updated
# 4. Verify git commit was created
# 5. Verify git push was successful
```

---

## 🔗 Import Statement

All scripts should add this import:

```python
from git_helpers import (
    is_base_branch_exists,
    clone_single_branch_and_checkout,
    clone_branch_and_checkout_new_branch,
    clone_repo_and_checkout,
    stage_commit_and_push,
    stage_specific_files_commit_and_push,
    configure_git_user,
    run_git_command,
    inject_git_token
)
```

---

## 📁 Files Structure

```
backend/app/cd/scripts/
├── git_helpers.py                    ← Central git operations
├── promotion_branch_manager.py       ← ✅ UPDATED
├── values-promotion.py               ← TO UPDATE
├── create-release-note.py            ← TO UPDATE
├── generate-config.py                ← TO UPDATE
├── script.py                         ← TO UPDATE
└── app_db_infra_pull_services.py    ← TO UPDATE
```

---

## 💡 Quick Migration Steps for Other Scripts

1. **Add Import**
   ```python
   from git_helpers import clone_single_branch_and_checkout, configure_git_user, stage_commit_and_push
   ```

2. **Replace Clone Operations**
   ```python
   # OLD
   subprocess.run(["git", "clone", "--branch", branch_name, repo_url, target_folder], check=True)
   
   # NEW
   clone_single_branch_and_checkout(repo_url, branch_name, target_folder)
   ```

3. **Replace Git Config**
   ```python
   # OLD
   subprocess.run(['git', 'config', 'user.email', 'kranthimj23@gmail.com'], cwd=repo_path)
   subprocess.run(['git', 'config', 'user.name', 'kranthimj23'], cwd=repo_path)
   
   # NEW
   configure_git_user(repo_path)
   ```

4. **Replace Commit/Push**
   ```python
   # OLD
   subprocess.run(['git', 'add', '.'], cwd=repo_path)
   subprocess.run(['git', 'commit', '-m', 'message'], cwd=repo_path)
   subprocess.run(['git', 'push', 'origin', branch_name], cwd=repo_path)
   
   # NEW
   stage_commit_and_push(repo_path, branch_name, 'message')
   ```

---

## ✅ Status Summary

| Script | Status | Integration | Lines Removed |
|--------|--------|-------------|---------------|
| promotion_branch_manager.py | ✅ DONE | 100% | ~35 |
| values-promotion.py | ⏳ PENDING | 0% | ~50 |
| create-release-note.py | ⏳ PENDING | 0% | ~40 |
| generate-config.py | ⏳ PENDING | 0% | ~30 |
| script.py | ⏳ PENDING | 0% | ~25 |
| app_db_infra_pull_services.py | ⏳ PENDING | 0% | ~20 |
| **TOTAL** | | | **~200 lines** |

---

## 🎯 Next Action

Ready to integrate git_helpers into the remaining scripts?

Request format for remaining scripts:
- "Update values-promotion.py to use git_helpers"
- "Update create-release-note.py to use git_helpers"
- Etc.

---

**Integration Progress:** 1/6 scripts completed (16%)
**Estimated Completion:** 5 more integrations
**Total Code Reduction Target:** ~200 lines

