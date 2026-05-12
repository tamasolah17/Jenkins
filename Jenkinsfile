pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run App Test') {
            steps {
                sh 'python3 main.py'
            }
        }
    }
}