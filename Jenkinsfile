pipeline {
    agent any
    environment {
        PYTHON_EXEC = 'python3.12'  // Or adjust to 'python' if needed
        GIT_CREDENTIALS_ID = credentials('jenkins-token')
    }
 
    stages {
 
        stage('Checkout with credentials') {
            steps {
                deleteDir()
                script {
                    withCredentials([string(credentialsId: 'jenkins-token', variable: 'GIT_TOKEN')]) {
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/main"]],
                        userRemoteConfigs: [[
                            url: "${env.github_url}",
                            credentialsId: GIT_CREDENTIALS_ID
                        ]]
                        ])
                    }
                }
            }
        }
 
         
        stage('Load and Run script1.py') {
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
                                
                                // echo " Printing the value of result----"
                                // echo "$result"
                                // echo " Printed the value of result----"
                                
    
                                def (x1, x2, low, high, isNew) = result.tokenize(',').collect { it?.trim() ?: '' }
                                
                                
                                env.X1_BRANCH = x1
                                env.X2_BRANCH = x2
                                env.LOWER_ENV = low
                                env.HIGHER_ENV = high
                                env.NEW_BRANCH = isNew?.toLowerCase() ?: 'false'
                                // echo "This line is above lower_branch"
                                // echo "This is the repository: ${env.github_url}"
                                // echo "lower_branch= ${env.X1_BRANCH}"
                                // echo "This line is below lower_branch"
                                // echo "higher_branch= ${env.X2_BRANCH}"
                                // echo "LOWER_ENV= ${env.LOWER_ENV}"
                                // echo "HIGHER_ENV= ${env.HIGHER_ENV}"
                                // echo "Parsed NEW_BRANCH = ${env.NEW_BRANCH}"
                            }
                        }
                    }
                }
        }
 
        stage('Delay-1') {
            steps {
                echo "Waiting for 5 seconds..."
                sleep time: 5, unit: 'SECONDS'
            }
        }
 
        stage('Trigger Push-Files-To-Branch') {
                    steps {
                        script {
                            
                            if (env.NEW_BRANCH?.toLowerCase() == 'true') {
                                echo "Triggering Push-Files-To-Branch job for new branch: ${env.X2_BRANCH}"
        
                                configFileProvider([configFile(fileId: 'values-promotion', targetLocation: 'values-promotion.py')]) {
                                    withCredentials([string(credentialsId: 'jenkins-token', variable: 'GIT_TOKEN')]) {
                                    echo "${env.PYTHON_EXEC} values-promotion.py ${env.X2_BRANCH}"
                                    sh "${env.PYTHON_EXEC} values-promotion.py ${env.github_url} ${env.X2_BRANCH}"
                                    }
                                }
                            } else {
                                echo "Skipping Push-Files-To-Branch because NEW_BRANCH is not 'true'. Got: '${env.NEW_BRANCH}'"
                            }
                    }
            }
        }
 
        stage('Delay-2') {
            steps {
                echo "Waiting for 5 seconds..."
                sleep time: 5, unit: 'SECONDS'
            }
        }
 
        stage('Generate release-note for Application, DB and Infra') {
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
 
