pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/smeraagrawal/bookstore_project.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t bookstore_app .'
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker stop bookstore-container || true'
                    sh 'docker rm bookstore-container || true'
                    sh 'docker run -d -p 8501:8501 --name bookstore-container bookstore_app'
                }
            }
        }
    }
}
