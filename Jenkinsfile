pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run App Test') {
            steps {
                bat 'python -m py_compile Jenkins.py'
            }
        }

        stage('Deploy to EC2') {
            steps {
                bat '''
                ssh ubuntu@13.62.225.65 ^
                "cd /home/ubuntu/Jenkins && \
                git pull origin main && \
                source venv/bin/activate && \
                pip install -r requirements.txt && \
                sudo systemctl restart flaskapp"
                '''
            }
        }
    }
}