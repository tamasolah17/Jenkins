pipeline {
    agent any

    environment {
        REMOTE = "ubuntu@13.62.225.65"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/tamasolah17/Jenkins.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Test / Compile') {
            steps {
                sh 'python3 -m py_compile Jenkins.py'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                ssh -o StrictHostKeyChecking=no $REMOTE << 'EOF'
                cd /home/ubuntu/Jenkins || exit 1
                git pull origin main

                pip3 install -r requirements.txt

                sudo systemctl restart flaskapp
EOF
                '''
            }
        }
    }
}