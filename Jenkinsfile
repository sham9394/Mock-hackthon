pipeline {
    agent { label 'docker-agent' }   // 👈 your Jenkins agent label here

    environment {
        FRONT_IMAGE = "sham9394/frontend"
        BACK_IMAGE  = "sham9394/backend"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "📥 Cloning code from GitHub..."
                git branch: 'main', url: 'https://github.com/sham9394/Mock-hackthon.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "🐳 Building Frontend Image..."
                    frontendImage = docker.build("${FRONT_IMAGE}:${BUILD_NUMBER}", "./frontend")

                    echo "🐳 Building Backend Image..."
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

        stage('Deploy to Kubernetes') {
            steps {
                echo "🚀 Deploying all services to Kubernetes..."
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_FILE
                        kubectl apply -f k8s/mongodb-deployment.yaml
                        kubectl apply -f k8s/mongodb-service.yaml
                        kubectl apply -f k8s/backend-deployment.yaml
                        kubectl apply -f k8s/backend-service.yaml
                        kubectl apply -f k8s/frontend-deployment.yaml
                        kubectl apply -f k8s/frontend-service.yaml

                        echo "✅ Deployment Complete. Current Pods:"
                        kubectl get pods -o wide
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "🎉 CI/CD pipeline executed successfully!"
        }
        failure {
            echo "❌ CI/CD pipeline failed. Check logs."
        }
        always {
            echo "🏁 Pipeline completed (success or fail)."
        }
    }
}
