pipeline {
    agent any
    environment {
        IMAGE_VERSION = 'v1.2'  // your version here
        ECR_REPO = '195216432339.dkr.ecr.eu-west-3.amazonaws.com/weatherapp'
    }
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
                        sh "docker tag weatherapp/frontend:latest ${ECR_REPO}/frontend:${IMAGE_VERSION}"                    }
                    dir('backend'){
                        sh "docker build -t weatherapp/backend ."
                        sh "docker tag weatherapp/backend:latest ${ECR_REPO}/backend:${IMAGE_VERSION}"                    }
                }
            }
        }
        stage("Pushing image to dockerhub + ecr"){
            steps{
                dir('weather-app') {
                    dir('frontend'){
                        sh "docker push ${ECR_REPO}/frontend:${IMAGE_VERSION}"                    }
                    dir('backend'){
                        sh "docker push ${ECR_REPO}/backend:${IMAGE_VERSION}"                    }
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

