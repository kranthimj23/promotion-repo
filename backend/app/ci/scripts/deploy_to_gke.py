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

def update_helm_chart_temp(repo_url, image_repo, image_tag, ns, microservice):
    github_token = os.getenv("GIT_TOKEN")
    if github_token and "github.com" in repo_url:
        # Inject token into repo URL (safe for HTTPS GitHub URLs)
        if repo_url.startswith("https://"):
            repo_url = repo_url.replace("https://", f"https://{github_token}@")
        else:
            raise ValueError("Unsupported repo_url format. Must start with https://")
    with tempfile.TemporaryDirectory() as tmpdirname:
        print(f"\n>>> Cloning dev branch of repo into temporary directory: {tmpdirname}")
        run_command(f"git clone --branch dev {repo_url} {tmpdirname}")
        run_command('git config user.name "kranthimj23"', cwd=tmpdirname)
        run_command('git config user.email "kranthimj23@gmail.com"', cwd=tmpdirname)
        os.chdir(tmpdirname)

        # Locate the correct values.yaml file
        print("path is",os.chdir(tmpdirname))
        #print(os.path.listdir(tmpdirname))
        values_path = os.path.join('helm-charts', 'dev-values')
        print(values_path)
        yaml_path = os.path.join(values_path, f"{microservice}.yaml")
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"No YAML file found for microservice: {microservice}")

        print(f"\n>>> Found YAML file: {yaml_path}")
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)

        if 'image' not in data or not isinstance(data['image'], dict):
            data['image'] = {}

        data['image']['repository'] = image_repo
        data['image']['tag'] = image_tag
        data['image']['imageName'] = image_repo:image_tag

        with open(yaml_path, 'w') as f:
            yaml.safe_dump(data, f)
            
        # Run Helm upgrade
        chart_path = os.path.join(tmpdirname, 'helm-charts')
        helm_cmd = (
            f"helm upgrade --install {microservice} {chart_path} -f {yaml_path} -n {ns} "
            f"--set image.repository={image_repo} --set image.tag={image_tag}"
        )
        run_command(helm_cmd)

        #Git add, commit, and push
        run_command(f"git add {yaml_path}", cwd=tmpdirname)
        commit_msg = f"Update image repository to {image_repo} and tag to {image_tag}"
        run_command(f'git commit -m "{commit_msg}"', cwd=tmpdirname)
        run_command("git push origin dev", cwd=tmpdirname)

        return yaml_path

def main():
    CLUSTER = "autopilot-cluster-1"
    ZONE = "us-central1"
    PROJECT_ID = "nice-virtue-463917-m0"

    if len(sys.argv) != 6:
        print("Usage: deploy_to_gke.py <namespace> <image_repo> <image_tag> <repo_url> <microservice>")
        sys.exit(1)

    ns = sys.argv[1]
    image_repo = sys.argv[2]
    image_tag = sys.argv[3]
    repo_url = sys.argv[4]
    microservice = sys.argv[5]

    print(f"CLUSTER={CLUSTER}, ZONE={ZONE}, PROJECT_ID={PROJECT_ID}")
    print(">>> Starting deployment script")
    print(f"CLUSTER: {CLUSTER} | ZONE: {ZONE} | PROJECT_ID: {PROJECT_ID} | NAMESPACE: {ns}")

    # Authenticate with GKE
    run_command(
        f"gcloud container clusters get-credentials {CLUSTER} --region {ZONE} --project {PROJECT_ID}"
    )
    print(">>> Cluster credentials configured")

    result = update_helm_chart_temp(repo_url, image_repo, image_tag, ns, microservice)
    print(f"\n>>> Deployment Complete. YAML updated at: {result}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n Deployment failed: {e}")
        sys.exit(1) 
