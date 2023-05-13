#! /bin/bash
yum update -y
yum install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user
# install docker-compose
curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
echo "${file("${path.module}/docker-compose.yml")}" > /home/ubuntu/docker-compose.yml
docker-compose -f /home/ubuntu/docker-compose.yml up -d
