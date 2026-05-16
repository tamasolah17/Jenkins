pipeline {
    agent any

    stages {
        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest
                '''
            }
        }
         stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-cicd .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker stop flask-cicd-container || true
                    docker rm flask-cicd-container || true

                    docker run -d \
                        --name flask-cicd-container \
                        -p 24000:24000 \
                        flask-cicd
                '''
            }
        }


    }
}