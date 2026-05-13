pipeline {
    agent any

    stages {

        stage('Clone Check') {
            steps {
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Test') {
            steps {
                sh '''
                . venv/bin/activate
                python -m py_compile Jenkins.py
                '''
            }
        }

        stage('Restart Flask App') {
            steps {
                sh '''
                sudo systemctl restart flaskapp
                sudo systemctl status flaskapp --no-pager
                '''
            }
        }

    }
}