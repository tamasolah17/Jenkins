pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/yourusername/python-ci-project.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh 'python3 --version'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }
    }
}