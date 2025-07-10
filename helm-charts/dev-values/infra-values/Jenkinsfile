pipeline {
    agent any

    environment {
        GIT_REPO_URL = 'https://github.com/kranthimj23/devops-lab-gke.git'
        BRANCH = 'DEV'
        TF_DIR = '.'  // root
        TFVARS_FILE = 'terraform.tfvars'
        GCP_KEY = '/var/lib/jenkins/keys/devops-ai-labs-1-ffe9cbe45593.json'
        PROJECT_ID = 'devops-ai-labs-1'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: "${BRANCH}", url: "${GIT_REPO_URL}"
                sh 'ls -la'
            }
        }

        stage('GCP Authentication') {
            steps {
                sh """
                    export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                    gcloud auth activate-service-account --key-file="${GCP_KEY}"
                    gcloud config set project ${PROJECT_ID}
                    gcloud auth list
                """
            }
        }

        stage('Check tfvars file') {
            steps {
                script {
                    if (!fileExists("${TFVARS_FILE}")) {
                        error "❌ File '${TFVARS_FILE}' not found in root directory."
                    } else {
                        echo "✅ Found terraform.tfvars in root"
                        sh "cat ${TFVARS_FILE}"
                    }
                }
            }
        }

        stage('Terraform Init') {
            steps {
                sh """
                    export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                    terraform init
                """
            }
        }

        stage('Terraform Plan') {
            steps {
                sh """
                    export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                    terraform plan -var-file=${TFVARS_FILE}
                """
            }
        }

        stage('Terraform Apply') {
            steps {
                sh """
                    export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                    terraform apply -auto-approve -var-file=${TFVARS_FILE}
                """
            }
        }

        stage('Terraform State Check') {
            steps {
                sh """
                    export GOOGLE_APPLICATION_CREDENTIALS=${GCP_KEY}
                    terraform state list || echo 'No state yet.'
                """
            }
        }
    }

    post {
        failure {
            echo '❌ Pipeline failed.'
        }
        success {
            echo '✅ Pipeline completed successfully.'
        }
    }
}
