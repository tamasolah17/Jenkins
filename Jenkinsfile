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

                    python3 -m py_compile Jenkins.py
                    pytest
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                    ssh -i ~/.ssh/jenkins_key \
                    -o StrictHostKeyChecking=no ubuntu@13.62.225.65 "
                        cd /home/ubuntu/Jenkins && \
                        git pull origin main && \
                        sudo systemctl restart flaskapp
                    "
                '''
            }
        }
    }
}