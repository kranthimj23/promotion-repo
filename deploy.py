import subprocess
import sys
import os
import tempfile
 
def git_clone(repository_url, destination_directory, branch):
    """
    Clones a Git repository to destination_directory.
    """
    try:
        print(f"Cloning repo {repository_url} into {destination_directory} ...")
        result = subprocess.run(
            ['git', 'clone', repository_url, destination_directory, '--branch', branch],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        print("Repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e.stderr}")
        sys.exit(1)
 
def deploy_service(text_file, env, env_namespace):
    
    with open(text_file, 'r') as file:
        first_col_values = file.readlines()
 
    for items in first_col_values:
        service = items.strip()
        env_namespace = env_namespace.strip()
 
        command = f"helm upgrade --install {service} helm-charts -f helm-charts/{env}-values/app-values/{service}.yaml -n {env_namespace}"
 
        result = subprocess.run(command, shell=True, check=True)
 
 
def main():
    if len(sys.argv) < 4:
        print("Usage: python deploy_script.py <env> <namespace> <repo_url>")
        sys.exit(1)
 
    env_name = sys.argv[1]
    namespace = sys.argv[1]
    repo_url = sys.argv[2]
    branch = sys.argv[3]
 
    github_token = os.getenv("GIT_TOKEN")
    if github_token and "github.com" in repo_url:
    # Inject token into repo URL (safe for HTTPS GitHub URLs)
        if repo_url.startswith("https://"):
            repo_url = repo_url.replace("https://", f"https://{github_token}@")
        else:
            raise ValueError("Unsupported repo_url format. Must start with https://")
 
 
    if not env_name:
        print("Error: ENV is not set.")
        sys.exit(1)
 
    if not namespace:
        print("Error: Namespace is not set.")
        sys.exit(1)
 
    # Create a temporary directory which is auto-deleted
    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repo in tmpdir
        git_clone(repo_url, tmpdir, branch)
 
        # Construct path to the environment-specific text file inside cloned repo
        text_file_path = os.path.join(tmpdir, f"helm-charts/{env_name}-values/app-values/{env_name}.txt")
        os.chdir(tmpdir)
        if not os.path.exists(text_file_path):
            print(f"Error: File {text_file_path} does not exist in the cloned repository.")
            sys.exit(1)
 
        # Run deployment
        deploy_service(text_file_path, env_name, namespace)
 
if __name__ == "__main__":
    main()
 
