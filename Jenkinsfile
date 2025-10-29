pipeline {
    agent { label 'Node' }

    environment {
        FRONT_IMAGE = "sham9394/frontend"
        BACK_IMAGE  = "sham9394/backend"
        SWARM_HOST  = "3.110.150.167"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Cloning code from GitHub..."
                git branch: 'main', url: 'https://github.com/sham9394/Mock-hackthon.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "Building Frontend Image..."
                    frontendImage = docker.build("${FRONT_IMAGE}:${BUILD_NUMBER}", "./frontend")

                    echo "Building Backend Image..."
                    backendImage = docker.build("${BACK_IMAGE}:${BUILD_NUMBER}", "./backend")
                }
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {
                        frontendImage.push()
                        frontendImage.push('latest')
                        backendImage.push()
                        backendImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy to Docker Swarm') {
            steps {
                echo "Deploying services to Docker Swarm on ${SWARM_HOST}..."
                withCredentials([
                    sshUserPrivateKey(credentialsId: 'swarm-ssh', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')
                ]) {
                    sh '''
                        set -e
                        mkdir -p ~/.ssh
                        chmod 700 ~/.ssh

                        # Add remote host to known_hosts
                        ssh-keyscan -H ${SWARM_HOST} >> ~/.ssh/known_hosts
                        chmod 644 ~/.ssh/known_hosts

                        echo "Testing SSH connection to Swarm Manager..."
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SSH_USER@${SWARM_HOST} "hostname && echo '✅ SSH Connection successful!'"

                        echo " Deploying Docker Stack on Swarm..."
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SSH_USER@${SWARM_HOST} "
                            cd /home/root/workspace/Fully-Automated-END-to-END-CICD-Pipeline &&
                            docker swarm init || true &&
                            docker pull ${FRONT_IMAGE}:latest &&
                            docker pull ${BACK_IMAGE}:latest &&
                            docker stack deploy -c docker-compose.yml 3tier_stack &&
                            echo '✅ Deployment Complete. Current services:' &&
                            docker service ls &&
                            echo ' Active containers:' &&
                            docker ps -a
                        "
                    '''
                }
            }
        }
    }

    post {
        success {
            echo " CI/CD pipeline executed successfully and deployed to Docker Swarm!"
        }
        failure {
            echo "❌CI/CD pipeline failed. Check Jenkins console logs."
        }
        always {
            echo "🏁 Pipeline completed (success or fail)."
        }
    }
}
