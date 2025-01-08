# aws-infrastructure-automation
Automated AWS infrastructure deployment using Python and Boto3. It covers EC2, S3, Lambda, Auto Scaling, ALB, CloudWatch, and SNS for scaling, monitoring, and notifications. This project demonstrates real-time application management and lifecycle automation on AWS.

# AWS Infrastructure Deployment:
This project automates the deployment of a dynamic web application infrastructure on AWS. The infrastructure includes EC2 instances, Auto Scaling Groups, Application Load Balancers (ALB), SNS for notifications, and Lambda functions for handling scaling events. It also integrates CloudWatch for real-time monitoring and alerting.

## Key Features:
- **EC2 Instance Deployment**: Automatically launches EC2 instances.
- **Auto Scaling Group**: Creates and manages an Auto Scaling Group to handle varying traffic loads.
- **Application Load Balancer (ALB)**: Distributes incoming traffic across the EC2 instances.
- **SNS Topics**: Monitors scaling and health events and sends notifications to an email address.
- **Lambda Function**: Processes notifications from SNS and logs the events.
- **CloudWatch Alarms**: Sets up alarms to scale out EC2 instances based on CPU utilization.

## Technologies Used:
- **AWS EC2**: For launching and managing virtual servers.
- **AWS S3**: For storing static web content.
- **AWS ALB (Application Load Balancer)**: For distributing traffic to EC2 instances.
- **AWS Auto Scaling**: For automatic scaling of EC2 instances based on load.
- **AWS SNS (Simple Notification Service)**: For sending notifications related to scaling and health events.
- **AWS Lambda**: For automating tasks triggered by SNS notifications.
- **AWS CloudWatch**: For real-time monitoring of EC2 instances and setting alarms.

## How to Deploy:
1. Clone or download the repository.
2. Set up your AWS credentials on your local machine.
3. Run the `whole_infrastructure.py` script to deploy the infrastructure.
4. After deployment, monitor the infrastructure and receive notifications about scaling and health events.

### Deployment Steps:
1. **Create S3 Bucket**: For static file storage.
2. **Launch EC2 Instances**: Automatically launched with a web server configuration.
3. **Create Load Balancer**: To distribute incoming traffic across EC2 instances.
4. **Configure Auto Scaling Group**: Automatically scales the EC2 instances based on traffic.
5. **Set up SNS Topics**: For sending notifications about scaling and health events.
6. **Create Lambda Function**: To process the SNS notifications.
7. **Configure CloudWatch Alarms**: To scale EC2 instances based on CPU usage.

## Prerequisites:
- Python 3.x
- Boto3 library (AWS SDK for Python)
- AWS credentials (Access Key ID and Secret Access Key)
