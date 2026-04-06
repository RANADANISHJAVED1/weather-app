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
                        sh "docker tag weatherapp/frontend:latest 195216432339.dkr.ecr.eu-west-3.amazonaws.com/weatherapp/frontend:v1.1"
                    }
                    dir('backend'){
                        sh "docker build -t weatherapp/backend ."
                        sh "docker tag weatherapp/frontend:latest 195216432339.dkr.ecr.eu-west-3.amazonaws.com/weatherapp/frontend:v1.1"
                    }
                }
            }
        }
        stage("Pushing image to dockerhub + ecr"){
            steps{
                dir('weather-app') {
                    dir('frontend'){
                        sh "docker push 195216432339.dkr.ecr.eu-west-3.amazonaws.com/weatherapp/frontend:v1.1"
                    }
                    dir('backend'){
                        sh "docker push 195216432339.dkr.ecr.eu-west-3.amazonaws.com/weatherapp/backend:v1.1"
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
                            kubectl apply -f ingress.yml
                        '''
                    }
                }
            }
        }
    }
}

