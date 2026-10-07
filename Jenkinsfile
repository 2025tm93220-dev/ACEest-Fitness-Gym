pipeline { 

    agent any 

    stages { 

        stage('Checkout') { 

            steps { 

                git 'https://github.com/2025tm93220-dev/ACEest-Fitness-Gym.git' 

            } 

        } 

        stage('Install') { 

            steps { 

                sh 'pip install -r requirements.txt' 

            } 

        } 

        stage('Test') { 

            steps { 

                sh 'pytest' 

            } 

        } 

        stage('Docker Build') { 

            steps { 

                sh 'docker build -t aceest-gym .' 

            } 

        } 

    } 

} 
