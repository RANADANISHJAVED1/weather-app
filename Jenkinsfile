pipeline {
    agent any
    stages {
        stage("Cleaning Pipeline"){
            steps{
                cleanWs()
            }
        }
        stage('Clone Project') {
            steps {
                sh "git clone https://github.com/RANADANISHJAVED1/weather-app.git"
            }
        }
        stage('Creating Docker Image') {
            steps {
                sh "ls"
                withCredentials([usernamePassword(credentialsId: 'docker', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh "docker login -u $user -p $pass"
                }
                dir('weather-app') {
                    dir('frontend'){
                        sh "docker build -t weatherapp/frontend ."
                        sh "docker tag weatherapp/frontend:latest 195216432339.dkr.ecr.eu-west-3.amazonaws.com/weatherapp/frontend:latest"
                    }
                    dir('backend'){
                        sh "docker build -t weatherapp/backend ."
                        sh "docker tag weatherapp/frontend:latest 195216432339.dkr.ecr.eu-west-3.amazonaws.com/weatherapp/frontend:latest"
                    }
                }
            }
        }
        stage("Pushing image to dockerhub + ecr"){
            steps{
                dir('weather-app') {
                    dir('frontend'){
                        sh "docker push 195216432339.dkr.ecr.eu-west-3.amazonaws.com/weatherapp/frontend:latest"
                    }
                    dir('backend'){
                        sh "docker push 195216432339.dkr.ecr.eu-west-3.amazonaws.com/weatherapp/backend:latest"
                    }
                }
            }
        }
        stage("Kubectl Deploy"){
            steps{
                dir('weather-app') {
                    dir('Kubernetes') {
                        sh '''
                            kubectl apply -f backend-deployment.yml
                            kubectl apply -f frontend-deployment.yml
                            kubectl apply -f services.yml
                        '''
                    }
                }
            }
        }
    }
}

