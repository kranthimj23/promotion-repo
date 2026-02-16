# values-promotion.py - Refactoring Summary

## What Was Changed

### Old Behavior (Before)
- Read application repositories from environment variable `app_repo_list`
- Required setting `$env:app_repo_list` with newline-separated URLs before running the script
- Command-line: `python values-promotion.py <promotion_repo> <target_branch>`

### New Behavior (After)
- Read application repositories from a **file** (default: `services_list.txt`)
- File contains one repository URL per line
- Command-line: `python values-promotion.py <services_list_file> <promotion_repo> <target_branch>`

## Files Modified

1. **backend/app/cd/scripts/values-promotion.py**
   - Updated argument parsing: 3 arguments instead of 2
   - Added file validation and error handling
   - Removed environment variable dependency for app repos
   - Fixed authentication token handling for repos

## Files Created

1. **services_list.txt** (Root directory)
   - Sample file containing three example repositories
   - Format: one URL per line (one repo per line)
   - Can be modified to add/remove/update repositories

2. **VALUES_PROMOTION_README.md** (Root directory)
   - Complete documentation on how to use the updated script
   - Includes examples, argument descriptions, error handling

## Updated Script Arguments

### Argument 0 (Script name)
- `values-promotion.py`

### Argument 1 (New)
- **Type:** string (file path)
- **Meaning:** Path to text file containing repository URLs
- **Example:** `services_list.txt` or `./repos/my-services.txt`

### Argument 2 (Previously Argument 1, now Argument 2)
- **Type:** string (HTTPS Git URL)
- **Meaning:** Promotion repository URL
- **Example:** `https://github.com/your-org/promotion-repo.git`

### Argument 3 (Previously Argument 2, now Argument 3)
- **Type:** string (branch name)
- **Meaning:** Target branch in promotion repo
- **Example:** `dev`, `dev2`, `feature/new-promotion`

## Usage Example (PowerShell)

### Old Way (No Longer Works)
```powershell
$env:app_repo_list = "https://github.com/org/service-a.git`nhttps://github.com/org/service-b.git"
python .\backend\app\cd\scripts\values-promotion.py https://github.com/org/promotion-repo.git dev
```

### New Way (Current)
```powershell
# Optional: Set GitHub token
$env:GIT_TOKEN = "your_token_here"

# Run with services_list.txt
python .\backend\app\cd\scripts\values-promotion.py .\services_list.txt `
  https://github.com/your-org/promotion-repo.git dev2
```

## Benefits

✅ **No environment variables needed** - Cleaner, easier to manage  
✅ **File-based configuration** - Easy to track changes in version control  
✅ **Better error handling** - Clear error messages if file not found or empty  
✅ **Improved readability** - Explicit file paths instead of environment variables  
✅ **Multiple lists supported** - Can have different services_list files for different scenarios  

## Validation

✓ Python syntax check passed  
✓ Script compiles without errors  
✓ All required imports present  
✓ Error handling for missing file  
✓ Error handling for empty file  
✓ Token injection logic preserved  

## Testing Recommendations

1. Test with sample services_list.txt
2. Verify error handling when file is missing
3. Verify error handling when file is empty
4. Test with private repositories (with GIT_TOKEN)
5. Test with public repositories (without GIT_TOKEN)
6. Verify branch creation and checkout logic
7. Verify YAML file collection from source repos
8. Verify file writing to promotion repo
9. Verify git commit and push

## Migration Guide

If you have existing scripts that call the old `values-promotion.py`:

**Before:**
```bash
python values-promotion.py https://github.com/org/promotion-repo.git dev
```

**After:**
```bash
# Create or update services_list.txt with your repos
python values-promotion.py ./services_list.txt https://github.com/org/promotion-repo.git dev
```

## Questions or Issues?

- Check VALUES_PROMOTION_README.md for detailed documentation
- Review services_list.txt for file format examples
- Ensure services_list.txt file exists before running the script
- Verify repository URLs are correct and accessible

