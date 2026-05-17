pipeline {
    agent any

    stages {

        stage('Clone Check') {
            steps {
                sh 'ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                python3 -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Test') {
            steps {
                sh '''
                . venv/bin/activate
                python3 -m py_compile app.py
                pytest
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                echo "Deploying via Git pull on EC2..."

                curl -X POST http://13.62.225.65:5000/deploy-hook || true
                '''
            }
        }
    }
}