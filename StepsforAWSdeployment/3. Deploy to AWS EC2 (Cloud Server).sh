# SSH into server
ssh -i my-api-key.pem ec2-user@52.15.208.206

# Inside EC2 Server
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
exit  # Reconnect for group change

# Reconnect & Deploy
sudo docker pull 859816906087.dkr.ecr.us-east-2.amazonaws.com/readmission-api:latest
sudo docker run -d -p 80:8000 859816906087.dkr.ecr.us-east-2.amazonaws.com/readmission-api:latest

# Check status
sudo docker ps