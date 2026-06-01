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
                sshagent(['ec2-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@13.60.182.62 "
                        cd ~/Jenkins &&
                        git pull &&
                        docker stop qr-container || true &&
                        docker rm qr-container || true &&
                        docker build -t qr . &&
                        docker run -d --name qr-container -p 9000:9000 qr

                         echo 'Waiting for application...'

                        for i in {1..30}; do
                            curl -f http://localhost:9000/health && exit 0
                            sleep 5
                        done

                        echo 'Application failed readiness check'
                        exit 1
                    "
                    '''
                }
            }
        }
    }
}