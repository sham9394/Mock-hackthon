pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'your-dockerhub-username'
        IMAGE_BACKEND = "${DOCKERHUB_USER}/backend:latest"
        IMAGE_FRONTEND = "${DOCKERHUB_USER}/frontend:latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Pulling source code..."
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "Building Docker images..."
                    sh 'docker build -t $IMAGE_BACKEND ./backend'
                    sh 'docker build -t $IMAGE_FRONTEND ./frontend'
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                    echo "$PASS" | docker login -u "$USER" --password-stdin
                    docker push $IMAGE_BACKEND
                    docker push $IMAGE_FRONTEND
                    docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG')]) {
                    sh '''
                    echo "Deploying to Kubernetes..."
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/mongodb-deployment.yaml
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/mongodb-service.yaml
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/backend-deployment.yaml
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/backend-service.yaml
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/frontend-deployment.yaml
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/frontend-service.yaml
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Pipeline failed. Please check the logs."
        }
    }
}
