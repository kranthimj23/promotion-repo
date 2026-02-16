# Git Helpers - Consolidated Git Operations

## Overview

`git_helpers.py` provides reusable git operations to eliminate code duplication across all scripts in the promotion and configuration management workflow.

## Functions

### 1. `is_base_branch_exists(repo_url, branch_name)`

Check if a branch exists in the remote repository.

**Parameters:**
- `repo_url` (str): Repository URL
- `branch_name` (str): Branch name to check

**Returns:**
- `bool`: True if branch exists, False otherwise

**Example:**
```python
from git_helpers import is_base_branch_exists

exists = is_base_branch_exists(
    "https://github.com/example/repo.git",
    "release/2.0.0"
)
if exists:
    print("Branch exists!")
```

---

### 2. `clone_single_branch_and_checkout(repo_url, branch_name, target_folder, depth=None)`

Clone a single branch from repository and checkout.

**Parameters:**
- `repo_url` (str): Repository URL
- `branch_name` (str): Branch to clone
- `target_folder` (str): Destination folder
- `depth` (int, optional): Clone depth for shallow clone

**Returns:**
- `str`: Path to cloned repository

**Raises:**
- `RuntimeError`: If clone fails

**Example:**
```python
from git_helpers import clone_single_branch_and_checkout

repo_path = clone_single_branch_and_checkout(
    repo_url="https://github.com/example/repo.git",
    branch_name="release/2.0.0",
    target_folder="/tmp/promotion-x",
    depth=1  # Shallow clone
)
print(f"Cloned to: {repo_path}")
```

---

### 3. `clone_branch_and_checkout_new_branch(repo_url, base_branch, new_branch, target_folder)`

Clone repository from base branch and create a new branch from it.

**Parameters:**
- `repo_url` (str): Repository URL
- `base_branch` (str): Base branch to clone from
- `new_branch` (str): New branch name to create
- `target_folder` (str): Destination folder

**Returns:**
- `str`: Path to repository with new branch checked out

**Raises:**
- `RuntimeError`: If clone or branch creation fails

**Example:**
```python
from git_helpers import clone_branch_and_checkout_new_branch

repo_path = clone_branch_and_checkout_new_branch(
    repo_url="https://github.com/example/repo.git",
    base_branch="release/1.0.0",
    new_branch="release/2.0.0",
    target_folder="/tmp/promotion-x-new"
)
print(f"Repository with new branch: {repo_path}")
```

---

### 4. `clone_repo_and_checkout(repo_url, branch_name, target_folder)`

Clone repository and checkout specified branch.

**Parameters:**
- `repo_url` (str): Repository URL
- `branch_name` (str): Branch to checkout
- `target_folder` (str): Destination folder

**Returns:**
- `str`: Path to cloned and checked out repository

**Raises:**
- `RuntimeError`: If clone fails

**Example:**
```python
from git_helpers import clone_repo_and_checkout

repo_path = clone_repo_and_checkout(
    repo_url="https://github.com/example/repo.git",
    branch_name="master",
    target_folder="/tmp/repo-master"
)
print(f"Cloned and checked out: {repo_path}")
```

---

### 5. `stage_commit_and_push(repo_path, branch_name, commit_message, files_to_stage=".", pull_before_push=True, use_rebase=True)`

Stage changes, commit with message, and push to branch.

**Parameters:**
- `repo_path` (str): Path to git repository
- `branch_name` (str): Branch to push to
- `commit_message` (str): Commit message
- `files_to_stage` (str, optional): Files to stage (default: "." for all)
- `pull_before_push` (bool, optional): Pull before push (default: True)
- `use_rebase` (bool, optional): Use rebase when pulling (default: True)

**Raises:**
- `RuntimeError`: If any git operation fails

**Example:**
```python
from git_helpers import stage_commit_and_push

stage_commit_and_push(
    repo_path="/tmp/promotion-x",
    branch_name="release/2.0.0",
    commit_message="Config files generated: release/2.0.0",
    files_to_stage=".",
    pull_before_push=True,
    use_rebase=True
)
```

---

### 6. `stage_specific_files_commit_and_push(repo_path, branch_name, commit_message, files_list, pull_before_push=True, use_rebase=True)`

Stage specific files, commit with message, and push to branch.

**Parameters:**
- `repo_path` (str): Path to git repository
- `branch_name` (str): Branch to push to
- `commit_message` (str): Commit message
- `files_list` (list): List of files to stage
- `pull_before_push` (bool, optional): Pull before push (default: True)
- `use_rebase` (bool, optional): Use rebase when pulling (default: True)

**Raises:**
- `RuntimeError`: If any git operation fails

**Example:**
```python
from git_helpers import stage_specific_files_commit_and_push

stage_specific_files_commit_and_push(
    repo_path="/tmp/promotion-x",
    branch_name="release/2.0.0",
    commit_message="Add meta-sheet update",
    files_list=["meta-sheet.xlsx"],
    pull_before_push=True,
    use_rebase=True
)
```

---

## Helper Functions

### `run_git_command(cmd, cwd=None, shell=True, timeout=30)`

Execute a git command and return output.

**Example:**
```python
from git_helpers import run_git_command

output = run_git_command(
    "git branch -r",
    cwd="/tmp/repo"
)
```

---

### `inject_git_token(repo_url, github_token=None)`

Inject GitHub token into repository URL for authentication.

**Example:**
```python
from git_helpers import inject_git_token

repo_with_token = inject_git_token(
    "https://github.com/example/repo.git",
    github_token="ghp_xxxx"
)
# Or use environment variable GIT_TOKEN
repo_with_token = inject_git_token("https://github.com/example/repo.git")
```

---

### `configure_git_user(repo_path, email="kranthimj23@gmail.com", name="kranthimj23")`

Configure git user.email and user.name for repository.

**Example:**
```python
from git_helpers import configure_git_user

configure_git_user(
    repo_path="/tmp/repo",
    email="user@example.com",
    name="User Name"
)
```

---

## Migration Guide

### Before (Without git_helpers)
```python
import subprocess
import os

# Repeated in multiple scripts
subprocess.run(['git', 'clone', '--branch', branch_name, repo_url, target_folder], check=True)
subprocess.run(['git', 'config', 'user.email', 'kranthimj23@gmail.com'], cwd=repo_path, check=True)
subprocess.run(['git', 'config', 'user.name', 'kranthimj23'], cwd=repo_path, check=True)
subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
subprocess.run(['git', 'commit', '-m', 'Update config'], cwd=repo_path, check=True)
subprocess.run(['git', 'push', 'origin', branch_name], cwd=repo_path, check=True)
```

### After (With git_helpers)
```python
from git_helpers import (
    clone_single_branch_and_checkout,
    configure_git_user,
    stage_commit_and_push
)

# Clean, reusable functions
repo_path = clone_single_branch_and_checkout(repo_url, branch_name, target_folder)
configure_git_user(repo_path)
stage_commit_and_push(repo_path, branch_name, "Update config")
```

---

## Benefits

✅ **Code Reusability** - No more duplicated git operations
✅ **Consistency** - Same git configuration across all scripts
✅ **Error Handling** - Centralized error handling and logging
✅ **Maintenance** - Changes to git operations only needed in one place
✅ **Testing** - Easier to test git operations independently
✅ **Documentation** - Clear function signatures and docstrings

---

## Error Handling

All functions raise `RuntimeError` on failure with detailed error messages:

```python
from git_helpers import clone_single_branch_and_checkout

try:
    repo_path = clone_single_branch_and_checkout(
        repo_url="https://invalid-url.git",
        branch_name="release/2.0.0",
        target_folder="/tmp/repo"
    )
except RuntimeError as e:
    print(f"Git operation failed: {e}")
    # Handle error appropriately
```

---

## Environment Variables

The module respects the following environment variables:

- **GIT_TOKEN**: GitHub personal access token for authentication
  ```bash
  export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

---

## Integration with Main Scripts

To use git_helpers in your scripts:

```python
# In promotion_branch_manager.py
from git_helpers import clone_single_branch_and_checkout, is_base_branch_exists

# In values_promotion.py
from git_helpers import clone_single_branch_and_checkout, configure_git_user, stage_commit_and_push

# In create_release_note.py
from git_helpers import clone_single_branch_and_checkout, configure_git_user, stage_commit_and_push

# In generate_config.py
from git_helpers import clone_single_branch_and_checkout, configure_git_user, stage_commit_and_push
```

---

## Testing

Example test for git_helpers:

```python
import tempfile
from git_helpers import clone_single_branch_and_checkout, is_base_branch_exists

def test_branch_exists():
    # Test with real GitHub repo
    exists = is_base_branch_exists(
        "https://github.com/kranthimj23/promotion-repo.git",
        "master"
    )
    assert exists == True

def test_clone_branch():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = clone_single_branch_and_checkout(
            repo_url="https://github.com/kranthimj23/promotion-repo.git",
            branch_name="master",
            target_folder=tmpdir
        )
        assert os.path.exists(repo_path)
        assert os.path.exists(os.path.join(repo_path, ".git"))
```

---

**Usage:** Import and use these functions in any script that needs git operations!

