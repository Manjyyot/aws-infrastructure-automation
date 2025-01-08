# AWS Infrastructure Automation

Automated AWS infrastructure deployment using Python and Boto3. This project simplifies the deployment of web application environments on AWS, with capabilities for scaling, monitoring, and notifications. It integrates AWS services such as EC2, S3, Lambda, Auto Scaling, ALB, CloudWatch, and SNS.

---

## Features
### 1. **End-to-End Infrastructure Deployment**
- Complete deployment of AWS resources using `deploy_infrastructure.py`.

### 2. **Individual Modules for Flexibility**
Each component of the infrastructure can be deployed individually using modular scripts:
- **S3 Bucket Creation**: `create_s3_bucket.py`
- **Launch EC2 Instances**: `launch_ec2_instance.py`
- **Set Up Application Load Balancer (ALB)**: `create_application_load_balancer.py`
- **Auto Scaling Group Configuration**: `create_auto_scaling_group.py`
- **SNS Notifications**: `setup_sns_notifications.py`
- **Lambda Function for SNS**: `process_sns_lambda_function.py`
- **CloudWatch Alarms**: `create_cloudwatch_alarms.py`

### 3. **Modular Deployment**
Use any individual module as needed without deploying the entire infrastructure.

---

## Deployment Instructions
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd aws-infrastructure-automation
