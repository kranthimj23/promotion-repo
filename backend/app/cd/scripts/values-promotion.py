import os
import stat
import shutil
import subprocess
from pathlib import Path
import tempfile
import sys
 
# ------------------ CONFIGURATION ------------------ #
app_raw_list = os.getenv('app-repo-list', '')
app_repo_list = [item.strip() for item in app_raw_list.split('\n') if item.strip()]
print("Parsed list:", app_repo_list)
 
aql_db_raw_list = os.getenv('aql-db-repo-list', '')
aql_db_repo_list = [item.strip() for item in aql_db_raw_list.split('\n') if item.strip()]
print("Parsed list:", aql_db_repo_list)
 
sql_db_raw_list = os.getenv('sql-db-repo-list', '')
sql_db_repo_list = [item.strip() for item in sql_db_raw_list.split('\n') if item.strip()]
print("Parsed list:", sql_db_repo_list)
 
infra_raw_list = os.getenv('infra-repo-list', '')
infra_repo_list = [item.strip() for item in infra_raw_list.split('\n') if item.strip()]
print("Parsed list:", infra_repo_list)
 
promotion_repo = sys.argv[1]
target_branch = sys.argv[2]
temp_dir = tempfile.mkdtemp()

github_token = os.getenv("GIT_TOKEN")
if github_token and "github.com" in promotion_repo:
    # Inject token into repo URL (safe for HTTPS GitHub URLs)
    if promotion_repo.startswith("https://"):
        promotion_repo = promotion_repo.replace("https://", f"https://{github_token}@")
    else:
        raise ValueError("Unsupported repo_url format. Must start with https://")
 
source_app_relative_path = os.path.join("helm-charts", "dev-values")
source_aql_relative_path = os.path.join("AQL", "scripts")
# source_sql_relative_path = os.path.join("SQL", "scripts")
# source_infra_relative_path = os.path.join("Infra")
 
destination_app_relative_path = os.path.join("helm-charts", "dev-values", "app-values")
destination_aql_relative_path = os.path.join("helm-charts", "dev-values", "db-scripts", "AQL")
# destination_sql_relative_path = os.path.join("helm-charts", "dev-values", "db-scripts", "SQL")
destination_infra_relative_path = os.path.join("helm-charts", "dev-values", "infra-values")
 
# ---------------------- FUNCTIONS ----------------------------- #
 
def run_git_command(cmd, cwd=None):
    print(f"Running: {cmd} in {cwd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=True, timeout=30)
    if result.returncode != 0:
        print(f" Git command failed:\nCommand: {cmd}\nReturn Code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
    return result.stdout.strip()
 
def prepare_promotion_repo(promotion_repo_url, workspace, branch):
    promo_repo_path = os.path.join(workspace, "promotion")
    try:
        print(f"Cloning promotion repo: {promotion_repo_url}")
        run_git_command(f"git clone {promotion_repo_url} promotion", cwd=workspace)
 
        remote_branches = run_git_command("git branch -r", cwd=promo_repo_path)
        print(f"Remote branches:\n{remote_branches}")
 
        if f"origin/{branch}" in remote_branches:
            print(f"Branch '{branch}' found. Checking it out.")
            run_git_command(f"git checkout {branch}", cwd=promo_repo_path)
        else:
            print(f"Branch '{branch}' not found. Creating from 'origin/main'.")
            run_git_command(f"git checkout -b {branch} origin/main", cwd=promo_repo_path)
 
        return promo_repo_path
    except subprocess.CalledProcessError as e:
        print(f"Error in prepare_promotion_repo: {e}\nOutput: {e.output}\nStderr: {e.stderr}")
        raise
 
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)
 
def main():
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
 
    collected_files = []
    collected_aql_files = []
    collected_sql_files = []
    collected_infra_dirs = []  # Store infra source directories for copying
 
    # ------------------ APP REPOS ------------------ #
    for repo in app_repo_list:
        try:
            if github_token and "github.com" in repo:
                # Inject token into repo URL (safe for HTTPS GitHub URLs)
                if repo.startswith("https://"):
                    repo = repo.replace("https://", f"https://{github_token}@")
                else:
                    raise ValueError("Unsupported repo_url format. Must start with https://")
            app_temp_dir = tempfile.mkdtemp()
            if os.path.exists(app_temp_dir):
                shutil.rmtree(app_temp_dir)
            os.makedirs(app_temp_dir)
            repo_name = Path(repo).stem
            repo_path = os.path.join(app_temp_dir, repo_name)
            run_git_command(f"git clone --branch main {repo}", cwd=app_temp_dir)
 
            source_path = os.path.join(repo_path, source_app_relative_path)
            print("Ssssooouurrccee", source_path)
            yaml_files = []
            if os.path.exists(source_path):
                yaml_files = [(f.name, f.read_text()) for f in Path(source_path).glob("*.yaml")]
            collected_files.extend(yaml_files)
            print(f"Fetched {len(yaml_files)} yaml files from {repo}")
 
        except Exception as e:
            print(f"Failed to fetch from {repo}: {e}")
 
    # ------------------ AQL REPOS ------------------ #
    for repo in aql_db_repo_list:
        try:
            if github_token and "github.com" in repo:
                # Inject token into repo URL (safe for HTTPS GitHub URLs)
                if repo.startswith("https://"):
                    repo = repo.replace("https://", f"https://{github_token}@")
                else:
                    raise ValueError("Unsupported repo_url format. Must start with https://")
            aql_temp_dir = tempfile.mkdtemp()
            if os.path.exists(aql_temp_dir):
                shutil.rmtree(aql_temp_dir)
            os.makedirs(aql_temp_dir)
            repo_name = Path(repo).stem
            repo_path = os.path.join(aql_temp_dir, repo_name)
            run_git_command(f"git clone --branch main {repo}", cwd=aql_temp_dir)
 
            source_path_aql = os.path.join(repo_path, source_aql_relative_path)
            aql_files = []
            if os.path.exists(source_path_aql):
                aql_files = [(f.name, f.read_text()) for f in Path(source_path_aql).glob("*.aql")]
            collected_aql_files.extend(aql_files)
            print(f"Fetched {len(aql_files)} aql files from {repo}")
 
        except Exception as e:
            print(f"Failed to fetch from {repo}: {e}")
 
    # ------------------ SQL REPOS (commented out) ------------------ #
    # for repo in sql_db_repo_list:
    #     try:
    #         sql_temp_dir = tempfile.mkdtemp()
    #         if os.path.exists(sql_temp_dir):
    #             shutil.rmtree(sql_temp_dir)
    #         os.makedirs(sql_temp_dir)
    #         repo_name = Path(repo).stem
    #         repo_path = os.path.join(sql_temp_dir, repo_name)
    #         run_git_command(f"git clone --branch main {repo}", cwd=sql_temp_dir)
 
    #         source_path_sql = os.path.join(repo_path, source_sql_relative_path)
    #         sql_files = []
    #         if os.path.exists(source_path_sql):
    #             sql_files = [(f.name, f.read_text()) for f in Path(source_path_sql).glob("*.sql")]
    #         collected_sql_files.extend(sql_files)
    #         print(f"Fetched {len(sql_files)} sql files from {repo}")
 
    #     except Exception as e:
    #         print(f"Failed to fetch from {repo}: {e}")
 
    # ------------------ INFRA REPOS ------------------ #
    for repo in infra_repo_list:
        try:
            if github_token and "github.com" in repo:
                # Inject token into repo URL (safe for HTTPS GitHub URLs)
                if repo.startswith("https://"):
                    repo = repo.replace("https://", f"https://{github_token}@")
                else:
                    raise ValueError("Unsupported repo_url format. Must start with https://")

            infra_temp_dir = tempfile.mkdtemp()
            if os.path.exists(infra_temp_dir):
                shutil.rmtree(infra_temp_dir)
            os.makedirs(infra_temp_dir)
            repo_name = Path(repo).stem
            repo_path = os.path.join(infra_temp_dir, repo_name)
            run_git_command(f"git clone --branch main {repo}", cwd=infra_temp_dir)
 
            source_path_infra = repo_path
            print(f"Infra source path: {source_path_infra}")
 
            collected_infra_dirs.append(source_path_infra)
 
        except Exception as e:
            print(f"Failed to fetch from {repo}: {e}")
 
    # ------------------ PREPARE PROMOTION REPO AND WRITE ------------------ #
    try:
        promo_repo_path = prepare_promotion_repo(promotion_repo, temp_dir, target_branch)
 
        destination_path = os.path.join(promo_repo_path, destination_app_relative_path)
        destination_aql_path = os.path.join(promo_repo_path, destination_aql_relative_path)
        # destination_sql_path = os.path.join(promo_repo_path, destination_sql_relative_path)
        destination_infra_path = os.path.join(promo_repo_path, destination_infra_relative_path)
 
        os.makedirs(destination_path, exist_ok=True)
        os.makedirs(destination_aql_path, exist_ok=True)
        # os.makedirs(destination_sql_path, exist_ok=True)
        os.makedirs(destination_infra_path, exist_ok=True)
 
        # Write YAML files
        for file_name, content in collected_files:
            dest_file_path = os.path.join(destination_path, file_name)
            with open(dest_file_path, 'x') as f:
                f.write(content)
 
        # Write AQL files
        for file_name, content in collected_aql_files:
            dest_aql_file_path = os.path.join(destination_aql_path, file_name)
            with open(dest_aql_file_path, 'x') as f:
                f.write(content)
 
        # Copy infra directories (overwrite existing infra-values folder)
        for infra_source_path in collected_infra_dirs:
            if os.path.exists(infra_source_path):
                print(f"Copying infra directory from {infra_source_path} to {destination_infra_path}")
 
                # Remove existing destination infra folder to avoid copytree error
                if os.path.exists(destination_infra_path):
                    shutil.rmtree(destination_infra_path)
 
                shutil.copytree(infra_source_path, destination_infra_path)
            else:
                print(f"Infra source path does not exist: {infra_source_path}")
 
        # Verification
        print("\nVerifying written files in promotion repo...\n")
        for file_name, _ in collected_files:
            dest_file_path = os.path.join(destination_path, file_name)
            if os.path.exists(dest_file_path):
                print(f"Found YAML: {dest_file_path}")
            else:
                print(f"Missing YAML file: {dest_file_path}")
 
        for file_name, _ in collected_aql_files:
            dest_aql_file_path = os.path.join(destination_aql_path, file_name)
            if os.path.exists(dest_aql_file_path):
                print(f"Found AQL: {dest_aql_file_path}")
            else:
                print(f"Missing AQL file: {dest_aql_file_path}")
 
        # for file_name, _ in collected_sql_files:
        #     dest_sql_file_path = os.path.join(destination_sql_path, file_name)
        #     if os.path.exists(dest_sql_file_path):
        #         print(f"Found SQL: {dest_sql_file_path}")
        #     else:
        #         print(f"Missing SQL file: {dest_sql_file_path}")
 
        for infra_dir in collected_infra_dirs:
            print(f"Infra directory copied from: {infra_dir}")
 
        # Commit and push changes
        subprocess.run(['git', 'config', 'user.email', 'kranthimj23@gmail.com'], cwd=promo_repo_path, check=True, timeout=30)
        subprocess.run(['git', 'config', 'user.name', 'kranthimj23'], cwd=promo_repo_path, check=True, timeout=30)
        run_git_command("git add .", cwd=promo_repo_path)
        run_git_command(f'git commit -m "Sync dev-values from all services"', cwd=promo_repo_path)
        run_git_command(f'git push origin {target_branch}', cwd=promo_repo_path)
 
        print("Promotion repository updated successfully.")
    except Exception as e:
        print(f"Failed to update promotion repo: {e}")
    finally:
        shutil.rmtree(temp_dir, onerror=remove_readonly)
 
if __name__ == "__main__":
    main()
 
 