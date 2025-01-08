import boto3
import time

# AWS Configuration
AWS_REGION = "us-east-1"  # Replace with your AWS region if needed
AMI_ID = "ami-03007fc8635b05e46"  # Amazon Linux 2 AMI (ensure this AMI is available in your region)
INSTANCE_TYPE = "t3.micro"  # Instance type
KEY_PAIR_NAME = "MAnjyotKeyPair"  # Your key pair name (without .pem)
EXISTING_SECURITY_GROUP_ID = "sg-06572b9fb25c29db9"  # Replace with your existing security group ID
VPC_SUBNET_IDS = ['subnet-01874c4512136bd62', 'subnet-08fa616f96d54dfc2']  # Subnets in your VPC

# User data script to install Apache and deploy a sample app
USER_DATA_SCRIPT = """#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<html><h1>Hello, this is your web app running on Apache!</h1></html>" > /var/www/html/index.html
"""

def create_launch_configuration(asg_client, launch_config_name, ami_id, instance_type, security_group_id, key_pair_name):
    """Creates a launch configuration for the Auto Scaling Group."""
    try:
        response = asg_client.create_launch_configuration(
            LaunchConfigurationName=launch_config_name,
            ImageId=ami_id,
            InstanceType=instance_type,
            SecurityGroups=[security_group_id],
            KeyName=key_pair_name,
            UserData=USER_DATA_SCRIPT,  # Configures Apache and deploys app
        )
        print(f"Launch configuration {launch_config_name} created successfully!")
        return response
    except Exception as e:
        print(f"Error creating launch configuration: {e}")
        return None

def create_auto_scaling_group(asg_client, asg_name, launch_config_name, vpc_zone_identifier):
    """Creates an Auto Scaling Group with the specified launch configuration."""
    try:
        response = asg_client.create_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            LaunchConfigurationName=launch_config_name,
            MinSize=1,
            MaxSize=5,
            DesiredCapacity=2,
            VPCZoneIdentifier=",".join(vpc_zone_identifier),  # Subnets for the ASG
            HealthCheckType='EC2',
            HealthCheckGracePeriod=300,
            Tags=[{
                'Key': 'Name',
                'Value': 'MyASGInstance',
                'PropagateAtLaunch': True
            }]
        )
        print(f"Auto Scaling Group {asg_name} created successfully!")
        return response
    except Exception as e:
        print(f"Error creating Auto Scaling Group: {e}")
        return None

def create_target_tracking_scaling_policy(asg_client, asg_name, policy_name, target_value):
    """Create a Target Tracking Scaling Policy for the Auto Scaling Group."""
    try:
        response = asg_client.put_scaling_policy(
            AutoScalingGroupName=asg_name,
            PolicyName=policy_name,
            PolicyType='TargetTrackingScaling',
            TargetTrackingConfiguration={
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ASGAverageCPUUtilization',  # You can use other metrics like NetworkOut, RequestCount
                },
                'TargetValue': target_value,  # Target value for the metric, e.g., 50% CPU utilization
                'DisableScaleIn': False,  # Enable scale-in
            }
        )
        print(f"Target Tracking Scaling Policy {policy_name} created successfully!")
        return response
    except Exception as e:
        print(f"Error creating Target Tracking Scaling Policy: {e}")
        return None

def main():
    # Initialize boto3 clients
    ec2 = boto3.client("ec2", region_name=AWS_REGION)
    asg_client = boto3.client("autoscaling", region_name=AWS_REGION)

    # Step 1: Create Launch Configuration with a different name if it exists
    launch_config_name = "my-launch-configuration-2"  # Modify the name if already exists
    create_launch_configuration(asg_client, launch_config_name, AMI_ID, INSTANCE_TYPE, EXISTING_SECURITY_GROUP_ID, KEY_PAIR_NAME)

    # Step 2: Create Auto Scaling Group with a different name if it exists
    asg_name = "my-auto-scaling-group-2"  # Modify the name if already exists
    create_auto_scaling_group(asg_client, asg_name, launch_config_name, VPC_SUBNET_IDS)

    # Step 3: Create Target Tracking Scaling Policy (maintain CPU utilization at 50%)
    scaling_policy_name = "cpu-target-policy"
    create_target_tracking_scaling_policy(asg_client, asg_name, scaling_policy_name, target_value=50)

if __name__ == "__main__":
    main()