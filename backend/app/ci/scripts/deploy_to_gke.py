import subprocess
import os
import sys
import tempfile
import yaml 
 
def run_command(cmd, cwd=None):
    print(f"\n>>> Running Command:\n{cmd}")
    print(f">>> Working Directory: {cwd or os.getcwd()}")
    try:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True, cwd=cwd, timeout=60)
        print(">>> STDOUT:\n", result.stdout)
        if result.stderr:
            print(">>> STDERR:\n", result.stderr)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed with exit code {result.returncode}")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Command timed out: {cmd}")
 
def update_helm_chart_temp(repo_url, image_repo, image_tag, ns):
    github_token = os.getenv("GIT_TOKEN")
    if github_token and "github.com" in repo_url:
        repo_url = repo_url.replace("https://", f"https://{github_token}@")
    
    with tempfile.TemporaryDirectory() as tmpdirname:
        print(f"Cloning dev branch of repo into temporary directory: {tmpdirname}")
        run_command(f"git clone --branch dev {repo_url} {tmpdirname}")
        run_command('git config --global user.name "kranthimj23"', cwd=tmpdirname)
        run_command('git config --global user.email "kranthimj23@gmail.com"', cwd=tmpdirname)

 
        values_path = os.path.join(tmpdirname, 'helm-charts', 'dev-values')
        if not os.path.exists(values_path):
            raise FileNotFoundError(f"File not found: {values_path}")
        yaml_path = None
        for i in os.listdir(values_path):
            if i.endswith(".yaml"):
                yaml_path = os.path.join(values_path, i)
                print(f"Found YAML file: {yaml_path}")
                break
 
        if yaml_path is None:
            raise FileNotFoundError("No YAML file found in dev-values directory")
 
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
 
        if 'image' not in data or not isinstance(data['image'], dict):
            data['image'] = {}
 
        data['image']['repository'] = image_repo
        data['image']['tag'] = image_tag
 
        with open(yaml_path, 'w') as f:
            yaml.safe_dump(data, f)
 
        # Push changes back to the repo
        #run_command(f"git add {yaml_path}", cwd=tmpdirname)
        #commit_msg = f"Update image repository to {image_repo} and tag to {image_tag}"
       # run_command(f'git commit -m "{commit_msg}"', cwd=tmpdirname)
       # run_command("git push origin dev1", cwd=tmpdirname)
 
        chart_path = os.path.join(tmpdirname, 'helm-charts')
 
        helm_cmd = (
            f"helm upgrade --install user {chart_path} -f {yaml_path} -n {ns} "
            f"--set image.repository={image_repo} --set image.tag={image_tag}"
        )
        run_command(helm_cmd)
 
        # Run the subprocess with stdout/stderr captured 
 
    return yaml_path
 
def main():
    CLUSTER = "demo-gke-cluster"
 
    ZONE = "asia-south1"
    PROJECT_ID = "devops-ai-labs-1"
    
    ns = sys.argv[1]
    image_repo = sys.argv[2]
    image_tag = sys.argv[3]
    repo_url = sys.argv[4]
    print(f"CLUSTER={CLUSTER}, ZONE={ZONE}, PROJECT_ID={PROJECT_ID}")
    if not all([CLUSTER, ZONE, PROJECT_ID]):
        raise EnvironmentError("Missing required environment variables: CLUSTER, ZONE, or PROJECT_ID")
    print(">>> Starting deployment script")
    print(f"CLUSTER: {CLUSTER} | ZONE: {ZONE} | PROJECT_ID: {PROJECT_ID} | NAMESPACE: {ns}")
    run_command(f"gcloud container clusters get-credentials demo-gke-cluster --region asia-south1 --project devops-ai-labs-1")
    print(">>> Cluster credentials configured")
 
    result = update_helm_chart_temp(repo_url, image_repo, image_tag, ns) 
 
    print(f">>> Updated YAML path: {result}")
 
    # run_command(f"kubectl get pods -n {ns}")
 
    print(">>> Deployment Completed")
 
if __name__ == "__main__":
 
    main() 
    