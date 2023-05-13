pipeline {
    agent any
    environment {
        EC2_PUBLIC_IP = ""
        KEY_PEM = "leipzig.pem"
    }

    stages {
        stage('Checkout') {
            steps {
                // Git repo'dan kodu çek
             git branch: 'main', url: 'https://github.com/SeferAhmet/test.git'
            }
        }
        stage('Terraform Init and Apply') {
            steps {
                script {
                    // Terraform'u başlat ve uygula
                    sh 'terraform init || exit 1'
                    sh 'terraform apply -auto-approve || exit 1'
                    EC2_PUBLIC_IP = sh(script: 'terraform output ec2_public_ip', returnStdout: true).trim()
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Docker imajını oluştur
                    sh 'docker build -t sefops . || exit 1'
                }
            }
        }
        stage('SSH to EC2') {
          steps {
              script {
                 // SSH özel anahtar dosyasının izinlerini düzelt
                  sh "chmod 400 ${KEY_PEM}"

                  sshagent(['387fd54f-6eb0-4134-8558-0e3569490b2c']) {
                   // SSH ile EC2'ye bağlanarak docker-compose.yml dosyasını kopyala
                      sh "scp -i ${KEY_PEM} -o StrictHostKeyChecking=no requirements.txt ec2-user@${EC2_PUBLIC_IP}:/home/ec2-user/requirements.txt"
                      sh "scp -i ${KEY_PEM} -o StrictHostKeyChecking=no app.py ec2-user@${EC2_PUBLIC_IP}:/home/ec2-user/app.py"
                      sh "scp -i ${KEY_PEM} -o StrictHostKeyChecking=no Dockerfile ec2-user@${EC2_PUBLIC_IP}:/home/ec2-user/Dockerfile"
                      sh "scp -i ${KEY_PEM} -o StrictHostKeyChecking=no docker-compose.yml ec2-user@${EC2_PUBLIC_IP}:/home/ec2-user/docker-compose.yml"

                     // SSH ile EC2'ye bağlanarak docker-compose.yml dosyasını çalıştır
                      sh "ssh -i ${KEY_PEM} -o StrictHostKeyChecking=no ec2-user@${EC2_PUBLIC_IP} 'docker-compose -f /home/ec2-user/docker-compose.yml up -d'"
        
                    }
                }   
            }
       }
   } 
}
