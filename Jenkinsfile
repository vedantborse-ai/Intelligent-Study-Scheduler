pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/yourusername/intelligent-study-scheduler.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t scheduler-app .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop scheduler || true
                docker rm scheduler || true
                docker run -d -p 8000:8000 --name scheduler scheduler-app
                '''
            }
        }
    }
}
