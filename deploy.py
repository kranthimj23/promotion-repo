import subprocess

def deploy_service(text_file, env, env_namespace):

    with open(text_file, 'r') as file:

        first_col_values = file.readlines()

    # Execute Helm upgrade for each unique service in the first column

    for items in first_col_values:

        service = items.split(":")[0].strip()

        microservices = items.split(":")[1].strip()

        env_namespace = env_namespace.strip()

        command = f"helm upgrade --install {microservices} helm-charts -f helm-charts/{env}-values/{service}.yaml -n {env_namespace}"

        result = subprocess.run(command, shell=True, check=True)

        print(f"{service} : {microservices} end")

    return result

 


def main():

    env_name = "sit"

    namespace = "sit"

    if not env_name:

        print("Error: ENV is not set.")

    # if not channel_name:

    #     print("Error: CHANNEL is not set.")

    text_file_path = rf"helm-charts/{env_name}-values/app-values/{env_name}.txt"

    deployment = deploy_service(text_file_path, env_name, namespace)
 
if __name__ == "__main__":

    main()
