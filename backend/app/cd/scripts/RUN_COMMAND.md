# 🚀 RUN COMMAND - main.py

## ⚡ Direct Copy-Paste Command

```bash
python main.py dev sit https://github.com/kranthimj23/promotion-repo.git 2.0.0 services_list.txt release/1.0.0
```

---

## 📋 Full Template

```bash
python main.py <lower-env> <higher-env> <promotional-repo> <new-version> <services-list> <promote-branch-x-1>
```

---

## 🔄 Real-World Examples

### Dev to SIT (v2.0.0)
```bash
python main.py dev sit https://github.com/kranthimj23/promotion-repo.git 2.0.0 services_list.txt release/1.0.0
```

### SIT to UAT (v2.0.1 - Patch)
```bash
python main.py sit uat https://github.com/kranthimj23/promotion-repo.git 2.0.1 services_list.txt release/2.0.0
```

### UAT to PROD (v2.1.0 - Minor)
```bash
python main.py uat prod https://github.com/kranthimj23/promotion-repo.git 2.1.0 services_list.txt release/2.0.1
```

---

## 📝 Customization Guide

Replace these values with yours:

```
Position 1: dev              → Your LOWER environment
Position 2: sit              → Your HIGHER environment
Position 3: https://...git   → Your promotional repo URL
Position 4: 2.0.0            → Your release version
Position 5: services_list.txt → Your services file
Position 6: release/1.0.0    → Previous release branch
```

---

## ✅ Step-by-Step Setup

### 1️⃣ Navigate to Script Directory
```bash
cd backend/app/cd/scripts
```

### 2️⃣ Create services_list.txt
```bash
cat > services_list.txt << EOF
https://github.com/kranthimj23/service-admin.git
https://github.com/kranthimj23/service-user.git
https://github.com/kranthimj23/service-auth.git
EOF
```

### 3️⃣ Set GitHub Token (Optional)
```bash
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4️⃣ Run the Command
```bash
python main.py dev sit https://github.com/kranthimj23/promotion-repo.git 2.0.0 services_list.txt release/1.0.0
```

---

## 📊 What Gets Auto-Generated

**You specify:**
- `--new-version 2.0.0`

**Script auto-generates:**
- `--target-branch release/2.0.0`
- `--promote-branch-x release/2.0.0`

---

## 🔍 Verify Before Running

Before executing, check:
- ✅ You're in `backend/app/cd/scripts/` directory
- ✅ `services_list.txt` exists
- ✅ All repository URLs are correct
- ✅ Environments follow proper hierarchy (dev < sit < uat < prod)
- ✅ Version number is in X.Y.Z format

---

## 🎯 Expected Output

```
================================================================================
  Pipeline Orchestration Started
================================================================================

Parameters provided:
  Lower env: dev
  Higher env: sit
  Promotional repo: https://github.com/kranthimj23/promotion-repo.git
  New version: 2.0.0
  Services list: services_list.txt
  Promote branch x-1: release/1.0.0

Auto-generated branches from version 2.0.0:
  Target branch: release/2.0.0
  Promote branch-x: release/2.0.0

Services list file: services_list.txt
Found 3 services:
  1. https://github.com/kranthimj23/service-admin.git
  2. https://github.com/kranthimj23/service-user.git
  3. https://github.com/kranthimj23/service-auth.git

================================================================================
  Step 1/3: Running merger.py...
================================================================================
✅ merger.py completed successfully.

================================================================================
  Step 2/3: Running values-promotion.py...
================================================================================
✅ values-promotion.py completed successfully.

================================================================================
  Step 3/3: Running create-release-note.py...
================================================================================
✅ create-release-note.py completed successfully.

================================================================================
  Pipeline Completed Successfully
================================================================================

✅ All scripts executed successfully!
```

---

## 🆘 Troubleshooting

### Error: "Incorrect number of arguments"
**Solution:** Make sure you have exactly 6 arguments in this order:
```
1. lower-env
2. higher-env
3. promotional-repo (URL)
4. new-version
5. services-list (file)
6. promote-branch-x-1 (branch)
```

### Error: "Services list file not found"
**Solution:** Create services_list.txt in current directory:
```bash
cat > services_list.txt << EOF
https://github.com/kranthimj23/service-admin.git
EOF
```

### Error: "Git authentication failed"
**Solution:** Set GitHub token:
```bash
export GIT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Error: "Script not found"
**Solution:** Verify you're in the correct directory:
```bash
ls -la main.py merger.py values-promotion.py create-release-note.py
```

---

## 📈 Execution Time

- **Total:** 5-15 minutes
- **merger.py:** 2-3 minutes
- **values-promotion.py:** 2-5 minutes
- **create-release-note.py:** 2-5 minutes

---

## 📦 Generated Outputs

After successful completion:
- `release-note-<timestamp>.xlsx` - Release notes with changes
- `upgrade-services.txt` - Services to upgrade
- Git commits to promotional repository

---

## 🎉 You're Ready!

Just run this command and watch the pipeline execute:

```bash
python main.py dev sit https://github.com/kranthimj23/promotion-repo.git 2.0.0 services_list.txt release/1.0.0
```

For more details, see:
- `SYS_ARGV_GUIDE.md` - Detailed sys.argv usage
- `SIMPLIFIED_USAGE.md` - Simplified parameter overview
- `COMPLETION_SUMMARY.md` - Project completion summary

