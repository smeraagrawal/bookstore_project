pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning project from GitHub...'
                git branch: 'main', url: 'https://github.com/smeraagrawal/bookstore_project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t bookstore_app .'
            }
        }

        stage('Run Docker Container') {
            steps {
                echo 'Running Docker container...'
                sh 'docker stop bookstore-container || true'   // stop if exists
                sh 'docker rm bookstore-container || true'    // remove if exists
                sh 'docker run -d -p 8501:8501 --name bookstore-container bookstore_app'
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
