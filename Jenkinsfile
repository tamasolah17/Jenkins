pipeline {
    agent any

    environment {
        VENV = "/home/ubuntu/Jenkins/venv"
        APP_DIR = "/home/ubuntu/Jenkins"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'YOUR_GIT_REPO_URL'
            }
        }

        stage('Setup Python venv') {
            steps {
                sh '''
                python3 -m venv venv || true
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test / Compile') {
            steps {
                sh '''
                . venv/bin/activate
                python -m py_compile Jenkins.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                sudo systemctl restart flaskapp
                sudo systemctl status flaskapp --no-pager
                '''
            }
        }
    }
}