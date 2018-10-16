node {
    stage('Checkout'){
        checkout scm
    }
    stage('Build') {
        sh "docker-compose build --no-cache"
    }
    stage('Deploy') {
        sh "docker-compose up -d"
    }
}