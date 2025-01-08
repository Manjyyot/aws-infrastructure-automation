# AWS Infrastructure Automation

Automated AWS infrastructure deployment using Python and Boto3. This project simplifies the deployment of web application environments on AWS, with capabilities for scaling, monitoring, and notifications. It integrates AWS services such as EC2, S3, Lambda, Auto Scaling, ALB, CloudWatch, and SNS.

## Features

### 1. **End-to-End Infrastructure Deployment**
Deploys a complete infrastructure setup on AWS using the `deploy_infrastructure.py` script. This script automates the creation of all necessary resources, including EC2 instances, load balancers, auto-scaling groups, CloudWatch alarms, and more.

### 2. **Individual Modules for Flexibility**
Each component of the infrastructure can be deployed individually using modular scripts. These individual modules allow for granular control and flexibility in managing AWS resources.

- **S3 Bucket Creation**: `create_s3_bucket.py`  
  Creates an S3 bucket to store static web files.

- **Launch EC2 Instances**: `launch_ec2_instance.py`  
  Launches EC2 instances and configures them as web servers.

- **Set Up Application Load Balancer (ALB)**: `create_application_load_balancer.py`  
  Sets up an Application Load Balancer for distributing traffic across EC2 instances.

- **Auto Scaling Group Configuration**: `create_auto_scaling_group.py`  
  Configures an Auto Scaling Group (ASG) for scaling EC2 instances based on demand.

- **SNS Notifications**: `setup_sns_notifications.py`  
  Sets up Simple Notification Service (SNS) topics for alerts and notifications.

- **Lambda Function for SNS**: `process_sns_lambda_function.py`  
  Defines a Lambda function to process SNS notifications.

- **CloudWatch Alarms**: `create_cloudwatch_alarms.py`  
  Creates CloudWatch alarms to monitor CPU usage and other metrics for EC2 instances.

### 3. **Modular Deployment**
Use any individual module as needed without deploying the entire infrastructure, making the setup adaptable to different requirements.

---

## Deployment Instructions

### 1. Clone the repository

git clone [[repository-url](https://github.com/Manjyyot/aws-infrastructure-automation)].

cd aws-infrastructure-automation

## Deployment Instructions

### 2. Set up your AWS credentials
Make sure your AWS credentials are configured. You can:
- Configure your `~/.aws/credentials` file.
- Or set the environment variables:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_DEFAULT_REGION`

### 3. Run the complete deployment
To deploy the entire infrastructure, run the following command:
python deploy_infrastructure.py

Alternatively, if you want to deploy individual components, run the appropriate script:
python create_s3_bucket.py
python launch_ec2_instance.py
python create_application_load_balancer.py
python create_auto_scaling_group.py
python setup_sns_notifications.py
python process_sns_lambda_function.py
python create_cloudwatch_alarms.py
### 4. Monitor infrastructure
- Use AWS CloudWatch for monitoring resource utilization.
- Set up notifications via SNS for real-time updates.

---

## Prerequisites

Before running the scripts, ensure the following are installed:
- **Python 3.x**
- **AWS CLI configured** with proper IAM permissions
- **Boto3 library**:
pip install boto3

## Project Components

### Infrastructure Management

| Script                               | Description                                                                 |
|--------------------------------------|-----------------------------------------------------------------------------|
| `create_s3_bucket.py`                | Creates an S3 bucket to store static web files.                              |
| `launch_ec2_instance.py`            | Launches EC2 instances and configures them as web servers.                  |
| `create_application_load_balancer.py`| Sets up an Application Load Balancer for traffic distribution.              |
| `create_auto_scaling_group.py`       | Configures an Auto Scaling Group (ASG) for scaling EC2 instances.           |
| `create_cloudwatch_alarms.py`        | Creates CloudWatch alarms to monitor CPU usage and other metrics.           |
| `setup_sns_notifications.py`        | Sets up SNS topics for sending alerts and notifications.                    |
| `process_sns_lambda_function.py`    | Defines a Lambda function triggered by SNS notifications.                   |

### Automation

| Script                        | Description                                                               |
|-------------------------------|---------------------------------------------------------------------------|
| `deploy_infrastructure.py`     | Deploys the entire infrastructure setup, including all components.        |
| `automation_script.py`         | Automates deployment, monitoring, and teardown of AWS resources.          |

---

## Notes

- **Teardown**: Use the teardown script to destroy resources once they are no longer needed.
- **AWS Free Tier**: Ensure all AWS services used are within your AWS Free Tier limits to avoid unexpected charges.

---

By following these instructions, you will have a fully automated, scalable, and monitored AWS infrastructure ready for your web application needs!

