pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install') {
            steps { sh 'python3 -m pip install -r requirements.txt' }
        }
        stage('Build and Test') {
            steps {
                sh 'python3 -m py_compile app.py'
                sh 'pytest -q'
            }
        }
        stage('Docker Build') {
            steps { sh 'docker build --tag aceest-fitness:jenkins .' }
        }
    }

    post {
        always { cleanWs() }
    }
}
