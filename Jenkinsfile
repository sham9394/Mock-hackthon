pipeline {
    agent { label 'DK-slave' }   // 👈 Jenkins agent label

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
                        set -e
                        export KUBECONFIG=$KUBECONFIG_FILE

                        # Ensure Jenkins SSH environment is ready
                        mkdir -p ~/.ssh
                        chmod 700 ~/.ssh

                        # Automatically trust remote host
                        ssh-keyscan -H 13.233.194.223 >> ~/.ssh/known_hosts
                        chmod 644 ~/.ssh/known_hosts

                        echo "🔗 Testing SSH connection to Kubernetes master..."
                        ssh -o StrictHostKeyChecking=no root@13.233.194.223 "hostname && echo '✅ SSH Connection successful!'"

                        echo "📦 Starting Kubernetes deployment on remote server..."

                        ssh -o StrictHostKeyChecking=no root@13.233.194.223 "
                            cd /home/root/workspace/Automated_ETE_CICD_pipeline && \
                            export KUBECONFIG=/etc/kubernetes/admin.conf && \
                            kubectl apply -f k8s/mongodb-deployment.yaml && \
                            kubectl apply -f k8s/mongodb-service.yaml && \
                            kubectl apply -f k8s/backend-deployment.yaml && \
                            kubectl apply -f k8s/backend-service.yaml && \
                            kubectl apply -f k8s/frontend-deployment.yaml && \
                            kubectl apply -f k8s/frontend-service.yaml && \
                            echo '✅ Deployment Complete. Current Pods:' && \
                            kubectl get pods -o wide
                        "
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
