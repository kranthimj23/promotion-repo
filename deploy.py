import subprocess
import sys
import os

def deploy_service(text_file, env, env_namespace):
    with open(text_file, 'r') as file:
        first_col_values = file.readlines()

    for service in first_col_values:
        service = service.strip()
        env_namespace = env_namespace.strip()

        command = f"helm upgrade --install {service} helm-charts -f helm-charts/{env}-values/app-values/{service}.yaml -n {env_namespace}"
        print(f"Running command: {command}")

        result = subprocess.run(command, shell=True, check=True)
        print(f"Deployment for service {service} completed with return code {result.returncode}")

def main():
    if len(sys.argv) < 4:
        print("Usage: python deploy.py <env_namespace> <repo_url> <branch>")
        sys.exit(1)

    env_namespace = sys.argv[1]
    repo_url = sys.argv[2]  # unused here but kept for interface compatibility
    branch = sys.argv[3]    # unused here but kept for interface compatibility

    if not env_namespace:
        print("Error: env_namespace is not set.")
        sys.exit(1)

    # Since Jenkins already checked out the repo, no cloning here
    workspace = os.getcwd()

    # Compose the path to the environment-specific text file inside the workspace
    text_file_path = os.path.join(workspace, f"helm-charts/{env_namespace}-values/app-values/{env_namespace}.txt")
    print(f"Looking for deployment list file at: {text_file_path}")

    if not os.path.exists(text_file_path):
        print(f"Error: File {text_file_path} does not exist in the workspace.")
        sys.exit(1)

    deploy_service(text_file_path, env_namespace, env_namespace)

if __name__ == "__main__":
    main()
