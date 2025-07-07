//This script is written to implement the below steps:
//1) Traverse the meta-sheet to fetch the current and previous promotion branch or create a new branch if needed.
//2) Pulls all the files needed for deployment into the current promotion branch from the respective dev branch of service repos.
//3) Creates a release-note based on the diff between current and previous promotion branches.

 
pipeline {
    agent any // add your jenkins agent
    environment {
        PYTHON_EXEC = 'python3.12'  // Or adjust to 'python' if needed
        GIT_CREDENTIALS_ID = credentials('jenkins-token') //add your github credentials 
    }

    stages {
     stage('Set Git Config') {
            steps {
                script {
                    // Set Git username and email for Jenkins environment
                    sh "git config --global user.name 'kranthimj23'"
                    sh "git config --global user.email 'kranthimj23@gmail.com'"
                    sh "git config --list"
                }
            }
         }
                    
                    
                    
        stage('Checkout with credentials') {
            steps {
                deleteDir()
                script {
                    withCredentials([string(credentialsId: 'jenkins-token', variable: 'GIT_TOKEN')]) {
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: "*/dev"]],
                            userRemoteConfigs: [[
                                url: "https://${GIT_TOKEN}@github.com/kranthimj23/promotion-repo.git"
                            ]]
                        ])
                    }
                }
            }
        }

        stage('Fetch Branch') {
            steps {
                    configFileProvider([configFile(fileId: 'merger', targetLocation: 'merger.py')]) {
                        withCredentials([string(credentialsId: 'jenkins-token', variable: 'GIT_TOKEN')]) {
                            script {
                                def result = sh(
                                        script: "${env.PYTHON_EXEC} merger.py ${env.lower_env} ${env.higher_env} ${env.github_url} ${env.new_version}",
                                        returnStdout: true,
                                    ).trim()

                                    echo "Wait time of 5 secs"
                                    sleep time: 5, unit: 'SECONDS'

                                    def (x1, x2, low, high, isNew) = result.tokenize(',').collect { it?.trim() ?: '' }
                                    env.X1_BRANCH = x1
                                    env.X2_BRANCH = x2
                                    env.LOWER_ENV = low
                                    env.HIGHER_ENV = high
                                    env.NEW_BRANCH = isNew?.toLowerCase() ?: 'false'
                                }
                            }
                        }
                    }
        }

        stage('Wait1') {
            steps {
                echo "Waiting for 5 seconds..."
                sleep time: 5, unit: 'SECONDS'
            }
        }
      
        stage('New Baseline') {
            steps {
                script {
                    if (env.NEW_BRANCH?.toLowerCase() == 'true') {
                        echo "Triggering Push-Files-To-Branch job for new branch: ${env.X2_BRANCH}"
                        configFileProvider([configFile(fileId: 'values-promotion', targetLocation: 'values-promotion.py')]) {
                            withCredentials([string(credentialsId: 'jenkins-token', variable: 'GIT_TOKEN')]) {
                                echo "${env.PYTHON_EXEC} values-promotion.py ${env.X2_BRANCH}"
                                sh "${env.PYTHON_EXEC} values-promotion.py ${env.X2_BRANCH}"
                            }
                        }
                    } else {
                        echo "Skipping Push-Files-To-Branch because NEW_BRANCH is not 'true'. Got: '${env.NEW_BRANCH}'"
                    }
                }
            }
        }
 
        stage('Wait2') {  
            steps {
                echo "Waiting for 5 seconds..."
                sleep time: 5, unit: 'SECONDS'
            }
        }
 
        stage('Generate Release-note') {
                steps {
                    script {
                        if (env.X1_BRANCH && env.X2_BRANCH) {
                            configFileProvider([configFile(fileId: 'create-release-note', targetLocation: 'create-release-note.py'), configFile(fileId: 'database_scripts_merger', targetLocation: 'database_scripts_merger.py')]) {
                                withCredentials([string(credentialsId: 'jenkins-token', variable: 'GIT_TOKEN')]) {
                                    sh 'chmod +x database_scripts_merger.py'
                                    echo "create-release-note.py is getting executed with these parameters: ${env.X1_BRANCH} ${env.X2_BRANCH} ${env.LOWER_ENV} ${env.HIGHER_ENV} ${env.github_url}"
                                    sh "${env.PYTHON_EXEC} create-release-note.py ${env.X1_BRANCH} ${env.X2_BRANCH} ${env.LOWER_ENV} ${env.HIGHER_ENV} ${env.github_url} database_scripts_merger.py"
                                } 
                            }
                        } else {
                            echo "Skipping Push-Files-To-Branch because NEW_BRANCH is not 'true'. Got: '${env.NEW_BRANCH}'"
                        }
                }
            }
        }
    }
}
