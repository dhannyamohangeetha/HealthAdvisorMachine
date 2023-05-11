KAFKA FOR WINDOWS

# KAFKA_HOME
# java -version
1. Navigate to the Kafka installation directory
2. Start the ZooKeeper server by running the following command:
# 	bin\windows\zookeeper-server-start.bat config\zookeeper.properties
# This command will start the ZooKeeper server, which is required for Kafka to run.
3. Open another command prompt window and navigate to the Kafka installation directory as before.
# Start the Kafka server by running the following command:
# 	bin\windows\kafka-server-start.bat config\server.properties
# This command will start the Kafka server.
4. Open another command prompt window and navigate to the Kafka installation directory again
# Create a new topic by running the following command:
# 	bin\windows\kafka-topics.bat --create --zookeeper localhost:9092 --replication-factor 1 --partitions 1 --topic test
# This command will create a new topic named "test".
5. Start a Kafka producer by running the following command:
# 	bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic test
# This command will start a Kafka producer that can send messages to the "test" topic.
6. Start a Kafka consumer by running the following command:
# 	bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --from-beginning
# This command will start a Kafka consumer that can receive messages from the "test" topic.
7. In the Kafka producer command prompt window, type a message and press Enter. You should see the message
# appear in the Kafka consumer command prompt window.
-------------------------------------------------------------------------------------------

KAFKA FOR MAC

1. Start zookeeper
# zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
2. Start Kafka
# kafka-server-start /opt/homebrew/etc/kafka/server.properties
3. Create new topic name ‘test’
# kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
4. Start Kafka Producer that can send messages to ‘test’topic
# kafka-console-producer --broker-list localhost:9092 --topic test
5. Start Kafka consumer that can receive messages from ‘test’topic
# kafka-console-consumer --bootstrap-server localhost:9092 --topic test --from-beginning
# (‘Test’ is the name of the topic)
-------------------------------------------------------------------------------------------

DOCKER
1. Build
# docker build --tag passion-app .
2. Run
# docker run -it -e AWS_ACCESS_KEY_ID=... -e AWS_SECRET_ACCESS_KEY=... -e AWS_REGION=... -p5000:5000 passion-app:latest

 Docker Commands
#     docker build --tag passion-app .
#     docker run -it <image-name>
#     docker run -it -e AWS_ACCESS_KEY_ID=<access-key-id> -e AWS_SECRET_ACCESS_KEY=<secret-access-key>
#                     -e AWS_REGION=<region> <image-name>

Docker rregistry push
#     aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/f9g5b7l3
#     docker tag passion-app:latest public.ecr.aws/f9g5b7l3/passion-app:latest
#     docker push public.ecr.aws/f9g5b7l3/passion-app:latest
#
-------------------------------------------------------------------------------------------

KUBERNETES EKS
 EKS IN AWS
    Eks vpc template url:
#     https://soccerpassionproject.s3.amazonaws.com/EKS+kubernetes+files/amazon-eks-vpc-private-subnets.yaml
#
    Eks nodegroup template:
#     https://soccerpassionproject.s3.amazonaws.com/EKS+kubernetes+files/amazon-eks-nodegroup.yaml
#
    Download Auth config map:
#     curl -o aws-auth-cm.yaml https://soccerpassionproject.s3.amazonaws.com/EKS+kubernetes+files/aws-auth-cm.yaml
#
    CONFIG EKS
#     aws eks --region us-east-1 update-kubeconfig --name passion-app
-----------------------------------------------------------------------

EKS
1. Install AWS CLI
# curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# unzip awscliv2.zip
# sudo ./aws/install
#
2. Eks vpc template url:
# https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
#
3. Eks nodegroup template:
# https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/amazon-eks-nodegroup.yaml
#
4. Download Auth config map:
# curl -o aws-auth-cm.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-10-29/aws-auth-cm.yaml

APP FILES:
kubectl apply -f https://...

EKS ROLE
arn:aws:iam::245102284664:role/eksrole

Cluster ARN
arn:aws:eks:us-east-1:245102284664:cluster/passion-app

API server endpoint
https://BD13F4B29FF94FDD41624A485EC14E4A.gr7.us-east-1.eks.amazonaws.com

SecurityGroups
SubnetIds	4 subnets
VpcId

CONFIG EKS
aws eks --region us-east-1 update-kubeconfig --name passion-app (this is cluter name)
-------------------------------------------------------------------------------------------


COMMAND IN CLI TO DOWNLOAD FROM DYNAMODB
#     aws dynamodb scan --table-name comments --output json --query "Items[*]" > json/comments.json
-------------------------------------------------------------------------------------------

