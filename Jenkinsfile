pipeline {
    agent any 
    stages {
        stage('List repo') {
            steps {
                git url: 'https://github.com/trumans/selenium-cucumber-google.git'
                sh 'ls -R'
            }
        }
    }
}