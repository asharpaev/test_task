node {
    stage('Checkout'){
        checkout scm
    }
    stage('Build') {
        sh "docker-compose build --no-cache"
    }
    stage('Deploy') {
        sh "docker stack deploy --compose-file docker-compose.yml docker_logs"
    }
}
