import boto3
import time

# AWS Configuration
AWS_REGION = "us-east-1"  # Replace with your AWS region if needed
AMI_ID = "ami-0047ab179aa1f984f"  # Amazon Linux 2 AMI (ensure this AMI is available in your region)
INSTANCE_TYPE = "t3.micro"  # Instance type
KEY_PAIR_NAME = "MAnjyotKeyPair"  # Your key pair name (without .pem)
SECURITY_GROUP_ID = "sg-06572b9fb25c29db9"  # Replace with your existing security group ID
VPC_ID = "vpc-09f02049d6176fe30"  # Replace with your existing VPC ID

# User data script to install Apache and deploy a sample app
USER_DATA_SCRIPT = """#!/bin/bash
yum update -y
yum install -y httpd python3
pip3 install flask
systemctl start httpd
systemctl enable httpd
echo "<html><h1>Apache is running, but your Flask app will be deployed soon!</h1></html>" > /var/www/html/index.html
"""


def create_ec2_instance(ec2_resource):
    """Launches an EC2 instance with the specified configurations."""
    try:
        # Launch the instance using Security Group ID
        instance = ec2_resource.create_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_PAIR_NAME,
            SecurityGroupIds=[SECURITY_GROUP_ID],  # Use the existing security group ID
            MinCount=1,
            MaxCount=1,
            UserData=USER_DATA_SCRIPT,  # Configures Apache and deploys app
            SubnetId=get_default_subnet_id()  # Specify a subnet ID within the VPC
        )[0]

        print("Waiting for instance to initialize...")
        instance.wait_until_running()
        instance.reload()
        print(f"Instance {instance.id} is running. Public DNS: {instance.public_dns_name}")
        return instance
    except Exception as e:
        print(f"Error launching EC2 instance: {e}")
        return None

def get_default_subnet_id():
    """Fetch the default subnet ID for the specified VPC."""
    ec2 = boto3.client("ec2", region_name=AWS_REGION)
    subnets = ec2.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [VPC_ID]}])
    if subnets["Subnets"]:
        return subnets["Subnets"][0]["SubnetId"]
    else:
        raise Exception(f"No subnets found for VPC {VPC_ID}")

def main():
    ec2_resource = boto3.resource("ec2", region_name=AWS_REGION)

    # Step 1: Launch EC2 Instance
    instance = create_ec2_instance(ec2_resource)
    if instance:
        print(f"Web server deployed successfully! Access it at: http://{instance.public_dns_name}")
    else:
        print("Failed to deploy the web server.")

if __name__ == "__main__":
    main()
