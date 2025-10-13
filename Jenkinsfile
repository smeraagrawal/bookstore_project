pipeline {
    agent any

    environment {
        IMAGE_NAME = "bookstore_app"
        CONTAINER_NAME = "bookstore-container"
        PORT = "8501"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout correct branch from GitHub
                git branch: 'main', url: 'https://github.com/smeraagrawal/bookstore_project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Remove any existing container
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                    // Run new container
                    sh "docker run -d -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                }
            }
        }
    }
}
