pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            sh 'echo "Building"'
          }
        }
      }
    }
  
    stage('Test') {
      steps {
        sh 'echo "Testing stage" '
      }
    }
  
    stage('Deploy')
    {
      steps {
        echo "deploying the application"
      }
    }
  }
  
  post {
        always {
            echo 'The pipeline completed'
        }
        success {                   
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
}