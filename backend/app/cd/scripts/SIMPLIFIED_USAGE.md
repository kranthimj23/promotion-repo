# ✅ Main.py - UPDATED with Auto-Generated Branch Names

## 🎉 What Changed

The `main.py` script now **automatically generates branch names** from the `--new-version` parameter.

### Before (Old Way)
```bash
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

### After (New Way) ✨
```bash
python main.py \
    --lower-env dev \
    --higher-env sit \
    --promotional-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --promote-branch-x-1 release/1.0.0
```

---

## 📊 Simplified Parameters

### Required Parameters (5 total)
| Parameter | Purpose | Example |
|-----------|---------|---------|
| `--lower-env` | Source environment | `dev` |
| `--higher-env` | Target environment | `sit` |
| `--promotional-repo` | Repository URL | `https://github.com/kranthimj23/promotion-repo.git` |
| `--new-version` | Version (auto-generates branches) | `2.0.0` |
| `--services-list` | Services file path | `services_list.txt` |
| `--promote-branch-x-1` | Stable release branch | `release/1.0.0` |

### Auto-Generated Parameters (NO LONGER NEEDED)
These are now automatically created from `--new-version`:

- **`--target-branch`** → Auto-generated as `release/{new-version}`
- **`--promote-branch-x`** → Auto-generated as `release/{new-version}`

---

## 🔄 Auto-Generation Examples

When you pass `--new-version 2.0.0`, the script automatically generates:

```
Input:  --new-version 2.0.0
        ↓
Output: --target-branch release/2.0.0
        --promote-branch-x release/2.0.0
```

Other examples:
```
--new-version 2.0.1  → release/2.0.1
--new-version 2.1.0  → release/2.1.0
--new-version 3.0.0  → release/3.0.0
```

---

## 💡 Real-World Usage

### Example 1: Dev → SIT
```bash
python main.py \
    --lower-env dev \
    --higher-env sit \
    --promotional-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --promote-branch-x-1 release/1.9.0
```

**What happens automatically:**
- target-branch = `release/2.0.0`
- promote-branch-x = `release/2.0.0`

### Example 2: SIT → UAT (Patch Release)
```bash
python main.py \
    --lower-env sit \
    --higher-env uat \
    --promotional-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.0.1 \
    --services-list services_list.txt \
    --promote-branch-x-1 release/2.0.0
```

**What happens automatically:**
- target-branch = `release/2.0.1`
- promote-branch-x = `release/2.0.1`

### Example 3: UAT → PROD (Minor Release)
```bash
python main.py \
    --lower-env uat \
    --higher-env prod \
    --promotional-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.1.0 \
    --services-list services_list.txt \
    --promote-branch-x-1 release/2.0.1
```

**What happens automatically:**
- target-branch = `release/2.1.0`
- promote-branch-x = `release/2.1.0`

---

## 📋 Quick Reference

### Full Command Template
```bash
python main.py \
    --lower-env <env> \
    --higher-env <env> \
    --promotional-repo <url> \
    --new-version <version> \
    --services-list <file> \
    --promote-branch-x-1 <branch>
```

### Minimal Copy-Paste Example
```bash
python main.py \
    --lower-env dev \
    --higher-env sit \
    --promotional-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --promote-branch-x-1 release/1.0.0
```

---

## ✅ Pipeline Output

When you run the command, you'll see:

```
================================================================================
  Pipeline Orchestration Started
================================================================================

Script directory: /path/to/scripts

Auto-generated branches from version 2.0.0:
  Target branch: release/2.0.0
  Promote branch-x: release/2.0.0

Services list file: services_list.txt
Found 5 services:
  https://github.com/kranthimj23/service-admin.git
  https://github.com/kranthimj23/service-user.git
  https://github.com/kranthimj23/service-auth.git
  ... and 2 more

================================================================================
  Step 1/3: Running merger.py - Fetching branches and creating new branches if needed
================================================================================
...
✅ merger.py completed successfully.

================================================================================
  Step 2/3: Running values-promotion.py - Promoting configuration values
================================================================================
...
✅ values-promotion.py completed successfully.

================================================================================
  Step 3/3: Running create-release-note.py - Generating release notes
================================================================================
...
✅ create-release-note.py completed successfully.

================================================================================
  Pipeline Completed Successfully
================================================================================

✅ All scripts executed successfully!

Summary:
  ✓ Merged branches using merger.py
  ✓ Promoted values using values-promotion.py
  ✓ Generated release notes using create-release-note.py
```

---

## 🎯 Benefits of Auto-Generation

✅ **Fewer parameters** - Only 6 required instead of 8
✅ **Less error-prone** - No mismatches between branch names
✅ **Consistent naming** - All branches follow `release/X.Y.Z` format
✅ **Faster execution** - Less copy-paste errors
✅ **Clear intent** - Version number drives everything

---

## 🚀 Quick Start

### 1. Create services_list.txt
```bash
cat > services_list.txt << EOF
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
EOF
```

### 2. Run Pipeline
```bash
cd backend/app/cd/scripts

python main.py \
    --lower-env dev \
    --higher-env sit \
    --promotional-repo https://github.com/kranthimj23/promotion-repo.git \
    --new-version 2.0.0 \
    --services-list services_list.txt \
    --promote-branch-x-1 release/1.0.0
```

### 3. Monitor Output
Wait for ✅ success indicators for each script.

---

## 📝 Parameter Details

### `--new-version` (Controls Everything!)
- **Format:** Semantic versioning (X.Y.Z)
- **Examples:** `2.0.0`, `2.0.1`, `2.1.0`, `3.0.0`
- **Auto-generates:**
  - `--target-branch` as `release/X.Y.Z`
  - `--promote-branch-x` as `release/X.Y.Z`

### `--promote-branch-x-1` (Only Stable Branch You Specify)
- **Format:** `release/X.Y.Z`
- **Purpose:** Previous stable release for comparison
- **Example:** `release/1.0.0` (when promoting to `release/2.0.0`)

---

## 🔍 Verification

To verify the auto-generated branches are correct:

```bash
# Before running, you can check the output shows:
Auto-generated branches from version 2.0.0:
  Target branch: release/2.0.0
  Promote branch-x: release/2.0.0
```

---

## 🆘 Troubleshooting

### Error: "Services list file not found"
```bash
# Make sure services_list.txt exists
ls -la services_list.txt
```

### Error: "Branch not found"
```bash
# Verify the promote-branch-x-1 exists in promotional-repo
cd /path/to/promotional-repo
git branch -r | grep release
```

### Error: "Git authentication failed"
```bash
# Set GitHub token
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📚 Documentation

For more details, see:
- `MAIN_README.md` - Full overview
- `MAIN_QUICKSTART.md` - Quick examples
- `PARAMETER_REFERENCE_NEW.md` - Detailed parameter reference
- `COMMAND_BUILDER.md` - Interactive setup guide

---

**That's it! Much simpler now.** 🎉

Just specify the version, and everything else is auto-generated!

