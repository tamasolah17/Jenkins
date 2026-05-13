pipeline {
    agent any

    stages {

        stage('Clone Check') {
            steps {
                bat 'dir'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Test') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python -m py_compile Jenkins.py
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                bat '''
                ssh ubuntu@13.62.225.65 "cd /home/ubuntu/Jenkins && git pull origin main && sudo systemctl restart flaskapp"
                '''
            }
        }

    }
}