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

        stage('Deploy') {
            steps {
                sh '''
                ssh -i keys.pem ubuntu@13.60.182.62 "
                    cd ~/Jenkins &&
                    git pull &&
                    docker stop qr-container || true &&
                    docker rm qr-container || true &&
                    docker build -t qr . &&
                    docker run -d --name qr-container -p 9000:9000 qr
                "
                '''
            }
        }
    }
}