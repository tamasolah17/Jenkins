pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run App Test') {
            steps {
                sh '''
                python3 -m py_compile Jenkins.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                cd /home/ubuntu/Jenkins

                git pull origin main

                source venv/bin/activate

                pip install -r requirements.txt

                sudo systemctl restart flaskapp
                '''
            }
        }
    }
}