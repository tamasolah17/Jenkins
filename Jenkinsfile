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
                python -m pip install --upgrade pip
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

       stage('Deploy to EC2 (SSM)') {
            steps {
                bat '''
                aws ssm send-command ^
                --instance-ids "i-xxxx" ^
                --document-name "AWS-RunShellScript" ^
                --parameters commands=["cd /home/ubuntu/Jenkins && git pull origin main && sudo systemctl restart flaskapp"] ^
                --region eu-central-1
                '''
            }
       }
    }
}