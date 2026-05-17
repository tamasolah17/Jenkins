pipeline {
    agent any

    stages {

        stage('Setup Python') {
            steps {
                bat '''
                    python -m venv venv

                    call venv\\Scripts\\activate

                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate

                    pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t flask-cicd .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat '''
                    docker stop flask-cicd-container

                    docker rm flask-cicd-container

                    docker run -d ^
                        --name flask-cicd-container ^
                        -p 24000:24000 ^
                        flask-cicd
                '''
            }
        }

    }
}